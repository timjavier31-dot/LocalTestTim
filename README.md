# Full Stack Next.js Project

This project includes:

- Frontend built with Next.js App Router
- Welcome login page at `/`
- Backend SQL Server login API route at `src/app/api/login/route.ts`
- Tailwind CSS styling
- TypeScript and ESLint support

## SQL Server connection

The app is configured to connect to Microsoft SQL Server Express at `DESKTOP-5IK0H2G\\SQLEXPRESS` using Windows authentication.

When the login form is used, the backend will ensure a database named `TestApp` exists and a table named `Users` exists for user lookup.

The login API checks whether the submitted domain and username exist in `TestApp.Users` and verifies the password before returning a success or failure message.

## Available commands

- `npm install`
- `npm run dev`
- `npm run build`
- `npm start`
- `npm run lint`

---

## Python Tools

Standalone Python scripts for job hunting and web scraping. Located in the [`python-tools/`](./python-tools) folder.

### Requirements

```bash
pip install requests beautifulsoup4
```

### Scripts

| Script | Description |
|---|---|
| `job_tracker.py` | Interactive CLI to log and track job applications locally |
| `job_scraper.py` | Scrapes live listings from RemoteOK and OnlineJobs.ph, saves picks to the tracker |
| `scraper.py` | Generic reusable scraper — extracts any data from any site using CSS selectors |

### Quick start

```bash
# Track job applications
python python-tools/job_tracker.py

# Scrape jobs from RemoteOK or OnlineJobs.ph
python python-tools/job_scraper.py

# Scrape any website with CSS selectors
python python-tools/scraper.py --url https://example.com --select h2
python python-tools/scraper.py --url https://site.com/jobs \
  --container div.job-card \
  --field title h3 text \
  --field link a href \
  --out jobs.csv
```

See [`python-tools/README.md`](./python-tools/README.md) for full usage, all flags, and examples.
