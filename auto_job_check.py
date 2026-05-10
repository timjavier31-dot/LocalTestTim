import csv
import os
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("Missing: pip install requests")
    sys.exit(1)

TRACKER_FILE = "job_applications.csv"
FIELDS = ["id", "date_applied", "company", "role", "platform", "status", "notes"]
KEYWORDS = ["database", "sql", "postgresql", "mysql", "dba", "data engineer"]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_remoteok():
    print("Fetching jobs from RemoteOK...")
    r = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    return [j for j in data if isinstance(j, dict) and "position" in j]


def matches(job):
    text = " ".join([
        job.get("position", ""),
        job.get("company", ""),
        " ".join(job.get("tags", [])),
    ]).lower()
    return any(kw in text for kw in KEYWORDS)


def load_tracked_urls():
    if not os.path.isfile(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    urls = set()
    for row in rows:
        note = row.get("notes", "")
        url = note.split(" | ")[0].strip()
        if url:
            urls.add(url)
    return urls


def load_existing():
    if not os.path.isfile(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_new_jobs(new_jobs):
    existing = load_existing()
    next_id = max((int(r["id"]) for r in existing), default=0) + 1

    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(existing)
        for job in new_jobs:
            tags = ", ".join(job.get("tags", [])[:5])
            url = job.get("url", "")
            notes = url + (f" | {tags}" if tags else "")
            writer.writerow({
                "id": next_id,
                "date_applied": datetime.now().strftime("%Y-%m-%d"),
                "company": job.get("company", "Unknown"),
                "role": job.get("position", "Unknown"),
                "platform": "RemoteOK",
                "status": "New",
                "notes": notes,
            })
            next_id += 1


def main():
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print("-" * 50)

    try:
        all_jobs = fetch_remoteok()
    except requests.exceptions.RequestException as e:
        print(f"Fetch failed: {e}")
        sys.exit(1)

    matched = [j for j in all_jobs if matches(j)]
    tracked_urls = load_tracked_urls()
    new_jobs = [j for j in matched if j.get("url", "") not in tracked_urls]

    print(f"Matched: {len(matched)}  |  Already tracked: {len(matched) - len(new_jobs)}  |  New: {len(new_jobs)}")
    print()

    if new_jobs:
        print("New jobs found:")
        for job in new_jobs:
            print(f"  + {job.get('position')} at {job.get('company')}")
            print(f"    {job.get('url')}")
        save_new_jobs(new_jobs)
        print(f"\nSaved {len(new_jobs)} new job(s) to {TRACKER_FILE}")
    else:
        print("No new jobs found today.")


if __name__ == "__main__":
    main()
