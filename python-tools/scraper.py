#!/usr/bin/env python3
"""
Generic web scraper. Extract any data from any website using CSS selectors.

Quick extract (flat list):
  python scraper.py --url https://example.com --select h2

Structured extract (table with named columns):
  python scraper.py --url https://site.com/jobs \
    --container div.job-card \
    --field title  "h4"       text \
    --field link   "a"        href \
    --field salary ".salary"  text \
    --out jobs.csv

Paginated scrape (use {page} in URL):
  python scraper.py --url "https://site.com/list?page={page}" \
    --pages 1 5 \
    --container div.item \
    --field title "h3" text \
    --out results.json

Save a config and reuse it later:
  python scraper.py --url ... --field ... --save-config mysite.json
  python scraper.py --config mysite.json
"""

import argparse
import csv
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing: pip install requests beautifulsoup4")
    sys.exit(1)

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


# ── Fetch ──────────────────────────────────────────────────────────────────────

def fetch(url, headers):
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


# ── Extract ────────────────────────────────────────────────────────────────────

def get_attr(el, attr):
    """Pull a value from a BeautifulSoup element."""
    if attr == "text":
        return el.get_text(strip=True)
    if attr == "html":
        return str(el)
    return el.get(attr) or ""


def scrape_page(soup, container, fields):
    """
    fields: list of (name, selector, attr)
    container: CSS selector that wraps one 'row', or None.

    Container mode  — one row per container, fields extracted relative to it.
    Parallel mode   — fields extracted as independent lists then zipped.
    """
    if container:
        rows = []
        for c in soup.select(container):
            row = {}
            for name, sel, attr in fields:
                el = c if sel in (".", "self", "") else c.select_one(sel)
                row[name] = get_attr(el, attr) if el else ""
            rows.append(row)
        return rows

    # Parallel mode
    lists = {}
    for name, sel, attr in fields:
        lists[name] = [get_attr(e, attr) for e in soup.select(sel)]

    if not lists:
        return []
    length = max(len(v) for v in lists.values())
    return [
        {name: (vals[i] if i < len(vals) else "") for name, vals in lists.items()}
        for i in range(length)
    ]


# ── Output ─────────────────────────────────────────────────────────────────────

def detect_format(out_file, forced):
    if forced:
        return forced
    if out_file:
        ext = os.path.splitext(out_file)[1].lower()
        if ext == ".json":
            return "json"
        if ext == ".csv":
            return "csv"
    return "lines"


def write_output(rows, field_names, out_file, fmt):
    if fmt == "json":
        content = json.dumps(rows, indent=2, ensure_ascii=False)
        if out_file:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(content)

    elif fmt == "csv":
        if out_file:
            with open(out_file, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=field_names)
                w.writeheader()
                w.writerows(rows)
        else:
            w = csv.DictWriter(sys.stdout, fieldnames=field_names)
            w.writeheader()
            w.writerows(rows)

    else:  # lines
        for row in rows:
            print(" | ".join(str(v) for v in row.values()))


# ── Config ─────────────────────────────────────────────────────────────────────

def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_config(args, path):
    cfg = {}
    if args.url:
        cfg["url"] = args.url
    if args.container:
        cfg["container"] = args.container
    if args.field:
        cfg["fields"] = [
            {"name": f[0], "selector": f[1], "attr": f[2] if len(f) > 2 else "text"}
            for f in args.field
        ]
    if args.pages:
        cfg["pages"] = args.pages
    if args.delay != 1.0:
        cfg["delay"] = args.delay
    if args.out:
        cfg["out"] = args.out
    if args.format:
        cfg["format"] = args.format
    if args.limit:
        cfg["limit"] = args.limit
    if args.header:
        cfg["headers"] = {k: v for k, v in args.header}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"Config saved -> {path}", file=sys.stderr)


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        prog="scraper.py",
        description="Generic web scraper — extract anything with CSS selectors.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    g = p.add_argument_group("Target")
    g.add_argument("--url", metavar="URL",
                   help="Page to scrape. Use {page} as placeholder for pagination.")
    g.add_argument("--pages", nargs="+", type=int, metavar="N",
                   help="Page numbers: --pages 3  OR  --pages 1 10 (range)")
    g.add_argument("--delay", type=float, default=1.0, metavar="SECS",
                   help="Seconds between page requests (default: 1)")
    g.add_argument("--header", action="append", nargs=2, metavar=("KEY", "VALUE"),
                   help="Extra request header, e.g. --header Cookie 'session=abc'. Repeatable.")

    g = p.add_argument_group("Extraction")
    g.add_argument("--container", metavar="SELECTOR",
                   help="CSS selector for the repeating row wrapper (e.g. div.job-card).")
    g.add_argument("--field", action="append", nargs="+", metavar="VALUE",
                   help=("Named field: NAME SELECTOR [ATTR=text]. Repeatable. "
                         "ATTR options: text (default), html, href, src, or any HTML attribute. "
                         "Use selector '.' to reference the container element itself."))
    g.add_argument("--select", nargs="+", metavar="VALUE",
                   help="Quick extract: SELECTOR [ATTR=text]. Prints a plain list.")

    g = p.add_argument_group("Output")
    g.add_argument("--out", metavar="FILE",
                   help="Output file. Extension sets format: .csv, .json. Omit to print to stdout.")
    g.add_argument("--format", choices=["csv", "json", "lines"],
                   help="Force output format (overrides --out extension).")
    g.add_argument("--limit", type=int, metavar="N",
                   help="Stop after collecting N results.")

    g = p.add_argument_group("Config")
    g.add_argument("--config", metavar="FILE",
                   help="Load settings from a JSON config file.")
    g.add_argument("--save-config", dest="save_config", metavar="FILE",
                   help="Save current settings as a reusable JSON config file.")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Merge config file (CLI args take priority)
    if args.config:
        cfg = load_config(args.config)
        args.url = args.url or cfg.get("url")
        args.container = args.container or cfg.get("container")
        args.pages = args.pages or cfg.get("pages")
        args.delay = args.delay if args.delay != 1.0 else cfg.get("delay", 1.0)
        args.out = args.out or cfg.get("out")
        args.format = args.format or cfg.get("format")
        args.limit = args.limit or cfg.get("limit")
        if not args.field and "fields" in cfg:
            args.field = [
                [f["name"], f["selector"], f.get("attr", "text")]
                for f in cfg["fields"]
            ]
        if not args.header and "headers" in cfg:
            args.header = list(cfg["headers"].items())

    if not args.url:
        parser.error("--url is required (or use --config with a 'url' key)")

    # Build request headers
    headers = {"User-Agent": DEFAULT_UA}
    for k, v in (args.header or []):
        headers[k] = v

    # Normalize fields
    fields = []
    if args.field:
        for f in args.field:
            name = f[0]
            sel  = f[1] if len(f) > 1 else "."
            attr = f[2] if len(f) > 2 else "text"
            fields.append((name, sel, attr))

    # --select shorthand (single-field, no column name)
    quick_mode = False
    if args.select and not fields:
        sel  = args.select[0]
        attr = args.select[1] if len(args.select) > 1 else "text"
        fields = [("value", sel, attr)]
        quick_mode = True

    if not fields:
        parser.error("Provide --field NAME SELECTOR [ATTR]  or  --select SELECTOR [ATTR]")

    # Save config before scraping so errors don't block a save
    if args.save_config:
        save_config(args, args.save_config)

    # Build page list
    if args.pages:
        pages = (
            [args.pages[0]]
            if len(args.pages) == 1
            else list(range(args.pages[0], args.pages[1] + 1))
        )
    else:
        pages = [None]  # single fetch, no {page} substitution

    # Scrape
    all_rows = []
    for i, page in enumerate(pages):
        url = args.url.replace("{page}", str(page)) if page is not None else args.url
        print(f"Fetching: {url}", file=sys.stderr)

        try:
            soup = fetch(url, headers)
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}", file=sys.stderr)
            continue

        rows = scrape_page(soup, args.container, fields)
        all_rows.extend(rows)
        print(f"  {len(rows)} rows  ({len(all_rows)} total)", file=sys.stderr)

        if args.limit and len(all_rows) >= args.limit:
            all_rows = all_rows[: args.limit]
            break

        if i < len(pages) - 1:
            time.sleep(args.delay)

    if not all_rows:
        print("No results. Check your selectors.", file=sys.stderr)
        sys.exit(1)

    # Output
    fmt = detect_format(args.out, args.format)
    field_names = [f[0] for f in fields]

    if quick_mode:
        for row in all_rows:
            print(row.get("value", ""))
    else:
        write_output(all_rows, field_names, args.out, fmt)
        if args.out:
            print(f"Saved {len(all_rows)} rows -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
