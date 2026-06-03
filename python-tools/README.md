# Python Tools

Three standalone Python scripts for job hunting and web scraping. No paid API needed to run any of them.

---

## Requirements

```bash
pip install requests beautifulsoup4
```

Python 3.10 or higher.

---

## Scripts

### 1. `job_tracker.py` — Job Application Tracker

An interactive CLI for tracking every job you apply to. Saves to a local `job_applications.csv` file.

**Run:**
```bash
python job_tracker.py
```

**Menu options:**
```
1. Add new application   — enter company, role, platform, notes
2. View all applications — table showing all tracked jobs
3. Update status         — change a job's status by ID
4. Show summary          — count by status with a visual bar chart
5. Exit
```

**Statuses:** `Applied` → `Interview` → `Offer` / `Rejected` / `Ghosted`

**Output file:** `job_applications.csv` (created automatically on first use)

**Example session:**
```
=== JOB APPLICATION TRACKER ===

What do you want to do?
  1. Add new application

Company name: Acme Corp
Role/Position: AI Automation Specialist
Where did you apply?: LinkedIn
Notes: Requires N8N experience

Saved! AI Automation Specialist at Acme Corp added to your tracker.
```

---

### 2. `job_scraper.py` — Job Board Scraper → Tracker

Scrapes live job listings from **RemoteOK** and **OnlineJobs.ph**, lets you pick which ones to save, and writes them directly into `job_applications.csv`.

**Run:**
```bash
python job_scraper.py
```

**Step-by-step:**
```
Which site?
  1. RemoteOK
  2. OnlineJobs.ph
  3. Both

Enter number: 2
Search keyword: ai automation

Found 30 job(s) on OnlineJobs.ph:
#    Role                          Type       Salary       Tags
1    AI Workflow Specialist        Full Time  $800/mo      n8n, make, zapier
2    Virtual Assistant (AI Tools)  Part Time  $400/mo      chatgpt, claude
...

Which jobs to save? (e.g. 1,3  or  all  or  Enter to skip)
> 1,2

  + AI Workflow Specialist
  + Virtual Assistant (AI Tools)

2 job(s) saved from OnlineJobs.ph.
```

**Keywords to try:** `automation`, `n8n`, `ai`, `claude`, `make`, `zapier`, `virtual assistant`

> **Note:** OnlineJobs.ph hides company names until you apply — this is their policy, not a scraper limitation.

---

### 3. `scraper.py` — Generic Web Scraper

A reusable scraper that works on **any website**. You define what to extract using CSS selectors. Supports pagination, named columns, multiple output formats, and saved config files.

**Run:**
```bash
python scraper.py [options]
```

---

#### Quick extract — grab a flat list of elements

```bash
# All headlines from Hacker News
python scraper.py --url https://news.ycombinator.com --select ".titleline > a"

# All links from a page
python scraper.py --url https://example.com --select a href

# All image URLs
python scraper.py --url https://example.com --select img src
```

---

#### Structured extract — named columns saved to a file

```bash
python scraper.py \
  --url "https://www.onlinejobs.ph/jobseekers/jobsearch?q=automation" \
  --container "a[href*='/jobseekers/job/']" \
  --field title  "h4.fs-16"  text \
  --field salary "dd.col"    text \
  --field url    "."         href \
  --out jobs.csv
```

`--container` sets the CSS selector for the repeating wrapper (one per row).  
`--field NAME SELECTOR ATTR` defines each column. `ATTR` defaults to `text`; use `href`, `src`, or any HTML attribute name.  
Use `"."` as the selector to target the container element itself (e.g. to grab its `href`).

---

#### Paginated scrape

Put `{page}` anywhere in the URL and pass `--pages START END`:

```bash
python scraper.py \
  --url "https://example.com/jobs?page={page}" \
  --pages 1 5 \
  --delay 2 \
  --container "div.job-card" \
  --field title "h3"       text \
  --field link  "a.apply"  href \
  --out all_jobs.json
```

`--delay` adds a pause between pages (default: 1 second). Be polite to servers.

---

#### Save a config and reuse it

```bash
# Save
python scraper.py \
  --url "https://site.com/jobs" \
  --container div.card \
  --field title h3 text \
  --save-config mysite.json

# Reuse anytime (with optional overrides)
python scraper.py --config mysite.json
python scraper.py --config mysite.json --limit 20 --out today.csv
```

The saved `mysite.json` looks like:
```json
{
  "url": "https://site.com/jobs",
  "container": "div.card",
  "fields": [
    { "name": "title", "selector": "h3", "attr": "text" }
  ]
}
```

---

#### All options

| Flag | Description |
|---|---|
| `--url URL` | Target URL. Use `{page}` for pagination. |
| `--pages N` or `--pages N M` | Single page or range |
| `--delay SECS` | Pause between pages (default: 1) |
| `--header KEY VALUE` | Add a custom request header (repeatable) |
| `--container SELECTOR` | CSS selector for row wrapper |
| `--field NAME SEL [ATTR]` | Named column. ATTR: `text`, `href`, `src`, etc. (repeatable) |
| `--select SEL [ATTR]` | Quick flat-list extract |
| `--out FILE` | Output file (`.csv` or `.json`) |
| `--format csv\|json\|lines` | Force output format |
| `--limit N` | Stop after N rows |
| `--config FILE` | Load from saved config |
| `--save-config FILE` | Save current flags to config file |

---

#### How to find CSS selectors

1. Open the target website in Chrome or Firefox
2. Right-click the element you want → **Inspect**
3. Look at the `class` names and tag — e.g. `<div class="job-card">` → selector is `div.job-card`
4. For nested elements: `div.job-card h3.title`
5. For attribute matches: `a[href*="jobs"]` (href contains "jobs")

---

## File overview

```
python-tools/
├── job_tracker.py    # Interactive job application tracker (no internet needed)
├── job_scraper.py    # Scrapes RemoteOK + OnlineJobs.ph → saves to tracker
├── scraper.py        # Generic reusable scraper for any website
└── README.md         # This file
```

Output files (created at runtime, not committed):
- `job_applications.csv` — your job tracker data
- `leads.csv` — lead responder output (separate script)
