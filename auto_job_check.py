import csv
import os
import sys
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing: pip install requests beautifulsoup4")
    sys.exit(1)

TRACKER_FILE = "job_applications.csv"
FIELDS = ["id", "date_applied", "company", "role", "platform", "status", "notes"]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "")

REMOTEOK_KEYWORDS = ["fullstack", "full-stack", "sql", "database", "ai automation", "automation"]
ONLINEJOBS_KEYWORDS = ["fullstack", "sql database", "ai automation"]


# ── RemoteOK ──────────────────────────────────────────────────────────────────

def fetch_remoteok():
    print("Fetching RemoteOK...")
    r = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    return [j for j in data if isinstance(j, dict) and "position" in j]


def matches_remoteok(job, keywords):
    text = " ".join([
        job.get("position", ""),
        job.get("company", ""),
        " ".join(job.get("tags", [])),
    ]).lower()
    return any(kw in text for kw in keywords)


# ── OnlineJobs.ph ─────────────────────────────────────────────────────────────

def fetch_onlinejobs(keyword):
    print(f"Fetching OnlineJobs.ph for '{keyword}'...")
    url = f"https://www.onlinejobs.ph/jobseekers/jobsearch?q={requests.utils.quote(keyword)}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    job_links = soup.find_all("a", href=lambda h: h and "/jobseekers/job/" in h)

    jobs = []
    seen = set()
    for link in job_links:
        href = link.get("href", "")
        if href in seen:
            continue
        seen.add(href)

        h4 = link.find("h4", class_="fs-16")
        if not h4:
            continue

        badge = h4.find("span", class_="badge")
        job_type = badge.get_text(strip=True) if badge else "Any"
        if badge:
            badge.extract()
        title = h4.get_text(strip=True)

        salary_dd = link.find("dd", class_="col")
        salary = salary_dd.get_text(strip=True) if salary_dd else ""

        tag_links = link.find_all("a", class_="badge")
        tags = [t.get_text(strip=True) for t in tag_links]

        jobs.append({
            "title": title,
            "type": job_type,
            "salary": salary,
            "tags": tags,
            "url": "https://www.onlinejobs.ph" + href,
        })

    return jobs


# ── CSV helpers ───────────────────────────────────────────────────────────────

def load_tracked_urls():
    if not os.path.isfile(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {row.get("notes", "").split(" | ")[0].strip() for row in rows}


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
            writer.writerow({
                "id": next_id,
                "date_applied": datetime.now().strftime("%Y-%m-%d"),
                "company": job.get("company", "See URL"),
                "role": job.get("role", "Unknown"),
                "platform": job.get("platform", "Unknown"),
                "status": "New",
                "notes": job.get("notes", ""),
            })
            next_id += 1


# ── GitHub Issue notification ─────────────────────────────────────────────────

def create_github_issue(new_jobs):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("GitHub issue skipped: not running inside GitHub Actions.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    title = f"New Jobs Found ({len(new_jobs)}) — {today}"

    by_platform = {}
    for job in new_jobs:
        by_platform.setdefault(job.get("platform", "Unknown"), []).append(job)

    lines = [f"Found **{len(new_jobs)} new job(s)** matching your keywords on {today}.\n"]
    for platform, jobs in by_platform.items():
        lines.append(f"\n## {platform} ({len(jobs)} job(s))\n")
        for job in jobs:
            url = job.get("notes", "").split(" | ")[0].strip()
            role = job.get("role", "Unknown")
            company = job.get("company", "See URL")
            jtype = job.get("job_type", "")
            salary = job.get("salary", "")

            lines.append(f"### [{role}]({url})")
            lines.append(f"- **Company:** {company}")
            if jtype:
                lines.append(f"- **Type:** {jtype}")
            if salary:
                lines.append(f"- **Salary:** {salary}")
            lines.append(f"- **Link:** {url}\n")

    lines.append("\n---\n_Full list saved in `job_applications.csv` in this repo._")

    body = "\n".join(lines)
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    resp = requests.post(
        api_url,
        json={"title": title, "body": body, "labels": ["jobs"]},
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    print(f"GitHub issue created: {resp.json()['html_url']}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("AUTO JOB SCANNER")
    print("=" * 50)

    tracked_urls = load_tracked_urls()
    seen_urls = set(tracked_urls)
    all_new = []

    # RemoteOK
    try:
        ro_jobs = fetch_remoteok()
        ro_matched = [j for j in ro_jobs if matches_remoteok(j, REMOTEOK_KEYWORDS)]
        ro_new = [j for j in ro_matched if j.get("url", "") not in seen_urls]
        print(f"  matched: {len(ro_matched)}  new: {len(ro_new)}")
        for job in ro_new:
            url = job.get("url", "")
            seen_urls.add(url)
            tags = ", ".join(job.get("tags", [])[:5])
            all_new.append({
                "role": job.get("position", "Unknown"),
                "company": job.get("company", "Unknown"),
                "platform": "RemoteOK",
                "job_type": "",
                "salary": "",
                "notes": url + (f" | {tags}" if tags else ""),
            })
    except requests.exceptions.RequestException as e:
        print(f"RemoteOK failed: {e}")

    # OnlineJobs.ph
    for keyword in ONLINEJOBS_KEYWORDS:
        try:
            oj_jobs = fetch_onlinejobs(keyword)
            oj_new = [j for j in oj_jobs if j.get("url", "") not in seen_urls]
            print(f"  '{keyword}': found {len(oj_jobs)}  new: {len(oj_new)}")
            for job in oj_new:
                url = job.get("url", "")
                seen_urls.add(url)
                salary = job.get("salary", "")
                tags = ", ".join(job.get("tags", [])[:5])
                notes = url + (f" | {salary}" if salary else "") + (f" | {tags}" if tags else "")
                all_new.append({
                    "role": job.get("title", "Unknown"),
                    "company": "See URL",
                    "platform": "OnlineJobs.ph",
                    "job_type": job.get("type", "Any"),
                    "salary": salary,
                    "notes": notes,
                })
        except requests.exceptions.RequestException as e:
            print(f"OnlineJobs.ph '{keyword}' failed: {e}")

    print(f"\nTotal new jobs: {len(all_new)}")

    if all_new:
        for job in all_new:
            jtype = f" [{job['job_type']}]" if job.get("job_type") else ""
            print(f"  + [{job['platform']}]{jtype} {job['role']} — {job['company']}")
        save_new_jobs(all_new)
        print(f"Saved to {TRACKER_FILE}")
        create_github_issue(all_new)
    else:
        print("No new jobs found today.")


if __name__ == "__main__":
    main()
