# SQL Query Generator

A local, free AI-powered SQL tool built with Streamlit and Ollama. Type what you want in plain English and get SQL back — or connect to a live database and fetch results directly.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.58+-red) ![Ollama](https://img.shields.io/badge/Ollama-local-green)

---

## Features

- **Natural language → SQL** — describe what you want, get a query back
- **Live database connection** — connect to SQL Server, PostgreSQL, MySQL, or SQLite
- **Table browser** — see your tables and columns, preview top 5 rows instantly
- **Quick Fetch** — load all rows from a table with one click, no AI needed
- **Streaming output** — watch SQL generate token by token instead of waiting
- **CSV mode** — upload a CSV and query it without any database
- **Copy & download** — copy SQL to clipboard or download as `.sql` / `.csv`
- **Session history** — last 10 queries saved during your session
- **Runs 100% locally** — no API keys, no internet required, no cost

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/timjavier31-dot/LocalTestTim.git
cd LocalTestTim
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Pull an Ollama model**
```bash
ollama pull phi3
```
> `phi3` (~2.3 GB) is recommended for low-RAM machines. Use `llama3` (~4.7 GB) for better SQL quality if you have 16 GB+ RAM.

**4. Run the app**
```bash
streamlit run app.py
```
Or double-click `run.bat` on Windows.

The app opens automatically at `http://localhost:8501`.

---

## Database Support

| Database | Driver | Notes |
|---|---|---|
| SQL Server | `pyodbc` + ODBC Driver 17 | Windows Authentication (NTLM) supported |
| PostgreSQL | `psycopg2-binary` | Standard password auth |
| MySQL | `pymysql` | Standard password auth |
| SQLite | built-in | Provide the `.db` file path |

**SQL Server with Windows Authentication:**
- Check the **Windows Authentication (NTLM)** box — no username/password needed
- Uses your current Windows login automatically

---

## How to Use

### Generate SQL only
1. Paste your `CREATE TABLE` schema (or load a sample)
2. Describe what you want in plain English
3. Click **Generate SQL**
4. Copy or download the result

### Fetch from a connected database
1. Set **Data Source** → `Database` in the sidebar
2. Fill in connection details and click **Connect**
3. Your tables appear in the sidebar — click one to select it
4. Click **Quick Fetch** to instantly load all rows, or type a request and click **Fetch Data**
5. Results appear in an interactive table with a Download CSV button

### CSV mode
1. Set **Data Source** → `CSV Upload`
2. Upload one or more `.csv` files (filename = table name)
3. Describe your query and click **Generate & Run**

---

## Project Structure

```
sql-query-generator/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
├── run.bat           # Windows one-click launcher
└── .gitignore
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI |
| [Ollama](https://ollama.com) | Local LLM inference |
| [SQLAlchemy](https://sqlalchemy.org) | Database connection layer |
| [DuckDB](https://duckdb.org) | In-memory SQL for CSV queries |
| [sqlparse](https://github.com/andialbrecht/sqlparse) | SQL formatting |
| phi3 / llama3 | AI models (via Ollama) |
