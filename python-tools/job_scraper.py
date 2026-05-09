import csv
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    sys.exit(1)

TRACKER_FILE = "job_applications.csv"
FIELDS = ["id", "date_applied", "company", "role", "platform", "status", "notes"]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


# ── RemoteOK ──────────────────────────────────────────────────────────────────

def fetch_remoteok(keyword: str) -> list:
    print(f"\nFetching from RemoteOK for '{keyword}'...")
    r = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    all_jobs = [j for j in data if isinstance(j, dict) and "position" in j]

    kw = keyword.lower()
    matched = [
        j for j in all_jobs
        if kw in " ".join([
            j.get("position", ""),
            j.get("company", ""),
            " ".join(j.get("tags", [])),
        ]).lower()
    ]
    return matched if matched else all_jobs


def display_remoteok(jobs: list) -> None:
    print(f"\nFound {len(jobs)} job(s) on RemoteOK:\n")
    print(f"{'#':<4} {'Company':<22} {'Role':<38} {'Tags'}")
    print("-" * 95)
    for i, job in enumerate(jobs, 1):
        company = job.get("company", "Unknown")[:20]
        role = job.get("position", "Unknown")[:36]
        tags = ", ".join(job.get("tags", [])[:5])
        print(f"{i:<4} {company:<22} {role:<38} {tags}")


def save_remoteok(jobs: list, picks: list) -> int:
    apps = load_tracker()
    saved = 0
    for i in picks:
        job = jobs[i - 1]
        role = job.get("position", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")
        tags = ", ".join(job.get("tags", [])[:5])
        apps.append({
            "id": next_id(apps),
            "date_applied": datetime.now().strftime("%Y-%m-%d"),
            "company": company,
            "role": role,
            "platform": "RemoteOK",
            "status": "Applied",
            "notes": f"{url} | {tags}",
        })
        saved += 1
        print(f"  + {role} at {company}")
    save_tracker(apps)
    return saved


# ── OnlineJobs.ph ─────────────────────────────────────────────────────────────

def fetch_onlinejobs(keyword: str) -> list:
    print(f"\nFetching from OnlineJobs.ph for '{keyword}'...")
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

        # Title — strip the badge text (Full Time / Part Time)
        badge = h4.find("span", class_="badge")
        job_type = badge.get_text(strip=True) if badge else ""
        if badge:
            badge.extract()
        title = h4.get_text(strip=True)

        # Salary
        salary_dd = link.find("dd", class_="col")
        salary = salary_dd.get_text(strip=True) if salary_dd else ""

        # Skill tags
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


def display_onlinejobs(jobs: list) -> None:
    print(f"\nFound {len(jobs)} job(s) on OnlineJobs.ph:\n")
    print(f"{'#':<4} {'Role':<40} {'Type':<12} {'Salary':<25} {'Tags'}")
    print("-" * 105)
    for i, job in enumerate(jobs, 1):
        role = job["title"][:38]
        jtype = job["type"][:10]
        salary = job["salary"][:23]
        tags = ", ".join(job["tags"][:4])
        print(f"{i:<4} {role:<40} {jtype:<12} {salary:<25} {tags}")


def save_onlinejobs(jobs: list, picks: list) -> int:
    apps = load_tracker()
    saved = 0
    for i in picks:
        job = jobs[i - 1]
        role = job["title"]
        salary = job["salary"]
        tags = ", ".join(job["tags"][:5])
        notes = f"{job['url']}"
        if salary:
            notes += f" | {salary}"
        if tags:
            notes += f" | {tags}"
        apps.append({
            "id": next_id(apps),
            "date_applied": datetime.now().strftime("%Y-%m-%d"),
            "company": "See URL",
            "role": role,
            "platform": "OnlineJobs.ph",
            "status": "Applied",
            "notes": notes,
        })
        saved += 1
        print(f"  + {role}")
    save_tracker(apps)
    return saved


# ── Shared helpers ─────────────────────────────────────────────────────────────

def load_tracker() -> list:
    if not os.path.isfile(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_tracker(apps: list) -> None:
    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(apps)


def next_id(apps: list) -> int:
    if not apps:
        return 1
    return max(int(a["id"]) for a in apps) + 1


def parse_picks(choice: str, total: int) -> list:
    if choice == "all":
        return list(range(1, total + 1))
    picks = [int(x.strip()) for x in choice.split(",") if x.strip().isdigit()]
    return [p for p in picks if 1 <= p <= total]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("   JOB SCRAPER  ->  TRACKER")
    print("=" * 50)

    print("\nWhich site?")
    print("  1. RemoteOK")
    print("  2. OnlineJobs.ph")
    print("  3. Both")
    site_choice = input("\nEnter number: ").strip()

    keyword = input("Search keyword (e.g. automation, n8n, ai): ").strip()
    if not keyword:
        keyword = "automation"

    sources = []
    if site_choice in ("1", "3"):
        sources.append("remoteok")
    if site_choice in ("2", "3"):
        sources.append("onlinejobs")

    if not sources:
        print("Invalid choice.")
        return

    try:
        if "remoteok" in sources:
            jobs_ro = fetch_remoteok(keyword)
            if jobs_ro:
                display_remoteok(jobs_ro)
                print("\nWhich RemoteOK jobs to save? (e.g. 1,3  or  all  or  Enter to skip)")
                choice = input("> ").strip().lower()
                if choice:
                    picks = parse_picks(choice, len(jobs_ro))
                    if picks:
                        saved = save_remoteok(jobs_ro, picks)
                        print(f"\n{saved} job(s) saved from RemoteOK.")
            else:
                print("No RemoteOK results found.")

        if "onlinejobs" in sources:
            jobs_oj = fetch_onlinejobs(keyword)
            if jobs_oj:
                display_onlinejobs(jobs_oj)
                print("\nWhich OnlineJobs.ph jobs to save? (e.g. 1,3  or  all  or  Enter to skip)")
                choice = input("> ").strip().lower()
                if choice:
                    picks = parse_picks(choice, len(jobs_oj))
                    if picks:
                        saved = save_onlinejobs(jobs_oj, picks)
                        print(f"\n{saved} job(s) saved from OnlineJobs.ph.")
            else:
                print("No OnlineJobs.ph results found.")

    except requests.exceptions.RequestException as e:
        print(f"\nFetch failed: {e}")
        return

    print("\nDone! Run job_tracker.py to view your full list.")


if __name__ == "__main__":
    main()
