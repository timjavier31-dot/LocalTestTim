# LocalTestTim

A collection of local tools and projects.

---

## SQL Query Generator

A local, free AI-powered SQL tool built with Streamlit and Ollama. Type what you want in plain English and get SQL back — or connect to a live database and fetch results directly.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.58+-red) ![Ollama](https://img.shields.io/badge/Ollama-local-green)

### Features

- **Natural language → SQL** — describe what you want, get a query back
- **Live database connection** — connect to SQL Server, PostgreSQL, MySQL, or SQLite
- **Table browser** — see your tables and columns, preview top 5 rows instantly
- **Quick Fetch** — load all rows from a table with one click, no AI needed
- **Streaming output** — watch SQL generate token by token instead of waiting
- **CSV mode** — upload a CSV and query it without any database
- **Runs 100% locally** — no API keys, no internet required, no cost

### Setup

```bash
pip install -r requirements.txt
ollama pull phi3
streamlit run app.py
```

Or double-click `run.bat` on Windows.

### Database Support

| Database | Notes |
|---|---|
| SQL Server | Windows Authentication (NTLM) supported |
| PostgreSQL | Standard password auth |
| MySQL | Standard password auth |
| SQLite | Provide the `.db` file path |

---

## Full Stack Next.js Project

- Frontend built with Next.js App Router
- Welcome login page at `/`
- Backend SQL Server login API route at `src/app/api/login/route.ts`
- Tailwind CSS styling
- TypeScript and ESLint support

### SQL Server connection

Configured to connect to Microsoft SQL Server Express at `DESKTOP-5IK0H2G\\SQLEXPRESS` using Windows authentication. The login API checks whether the submitted domain and username exist in `TestApp.Users` and verifies the password before returning a success or failure message.

### Commands

```bash
npm install
npm run dev
npm run build
npm start
npm run lint
```

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
| `job_scraper.py` | Scrapes live listings from RemoteOK and OnlineJobs.ph |
| `scraper.py` | Generic reusable scraper — extracts any data from any site using CSS selectors |

### Quick start

```bash
python python-tools/job_tracker.py
python python-tools/job_scraper.py
python python-tools/scraper.py --url https://example.com --select h2
```

See [`python-tools/README.md`](./python-tools/README.md) for full usage and examples.
