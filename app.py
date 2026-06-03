import sys
sys.stdout.reconfigure(encoding="utf-8")

import streamlit as st
import streamlit.components.v1 as components
import ollama
import sqlparse
import html
import duckdb
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError

st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Query Generator")
st.caption("Natural language → SQL, powered by Ollama (local & free)")

# ── Session state defaults ────────────────────────────────────────────────────
for key, val in [
    ("schema", ""),
    ("query_request", ""),
    ("db_engine", None),
    ("db_tables", {}),      # {table_name: [col_defs]}
    ("selected_table", None),
    ("history", []),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Samples ───────────────────────────────────────────────────────────────────
SAMPLES = {
    "Job Applications Tracker": {
        "schema": """\
CREATE TABLE job_applications (
    id          INT PRIMARY KEY,
    date_applied DATE,
    company     VARCHAR(200),
    role        VARCHAR(200),
    platform    VARCHAR(100),
    status      VARCHAR(50),
    notes       TEXT
);""",
        "query": "Count total applications grouped by platform, sorted by most first"
    },
    "Customers & Orders": {
        "schema": """\
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    created_at TIMESTAMP
);
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total DECIMAL(10,2),
    status VARCHAR(20),
    ordered_at TIMESTAMP
);""",
        "query": "Show the top 5 customers by total order value in the last 30 days"
    },
}

DEFAULT_PORTS = {"PostgreSQL": "5432", "MySQL": "3306", "SQL Server": "1433"}

# ── DB helpers ────────────────────────────────────────────────────────────────
def build_url(db_type, host, port, database, user, password, windows_auth=False):
    if db_type == "PostgreSQL":
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    if db_type == "MySQL":
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    if db_type == "SQL Server":
        driver = "ODBC+Driver+17+for+SQL+Server"
        base = f"mssql+pyodbc://{host},{port}/{database}?driver={driver}"
        return base + ("&trusted_connection=yes" if windows_auth else f"&UID={user}&PWD={password}")
    if db_type == "SQLite":
        return f"sqlite:///{database}"

def load_db_tables(engine, db_type):
    """Returns {table_name: [{"name": col, "type": type}, ...]}"""
    inspector = inspect(engine)
    schema = "dbo" if db_type == "SQL Server" else None
    try:
        tables = inspector.get_table_names(schema=schema) if schema else inspector.get_table_names()
    except Exception:
        tables = inspector.get_table_names()

    result = {}
    for table in tables:
        try:
            cols = inspector.get_columns(table, schema=schema)
            try:
                pk_info = inspector.get_pk_constraint(table, schema=schema)
                pk_cols = set(pk_info.get("constrained_columns", [])) if isinstance(pk_info, dict) else set()
            except Exception:
                pk_cols = set()

            col_list = []
            for c in cols:
                if not isinstance(c, dict):
                    continue
                col_list.append({
                    "name": c.get("name", ""),
                    "type": str(c.get("type", "VARCHAR")),
                    "pk": c.get("name", "") in pk_cols,
                    "nullable": c.get("nullable", True),
                })
            result[table] = col_list
        except Exception:
            result[table] = []
    return result

def tables_to_schema(tables_dict):
    lines = []
    for table, cols in tables_dict.items():
        col_defs = []
        for c in cols:
            pk = " PRIMARY KEY" if c["pk"] else ""
            col_defs.append(f"    {c['name']} {c['type']}{pk}")
        lines.append(f"CREATE TABLE {table} (\n" + ",\n".join(col_defs) + "\n);")
    return "\n\n".join(lines)

def selected_table_schema(table_name, tables_dict):
    if table_name not in tables_dict:
        return ""
    cols = tables_dict[table_name]
    col_defs = []
    for c in cols:
        pk = " PRIMARY KEY" if c["pk"] else ""
        col_defs.append(f"    {c['name']} {c['type']}{pk}")
    return f"CREATE TABLE {table_name} (\n" + ",\n".join(col_defs) + "\n);"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    try:
        models = [m.model for m in ollama.list().models]
    except Exception:
        models = []

    if not models:
        st.error("Ollama not running.\n\n1. https://ollama.com\n2. `ollama pull phi3`\n3. Restart app")
        st.stop()

    selected_model = st.selectbox("Model", models)
    dialect_options = ["PostgreSQL", "MySQL", "SQLite", "SQL Server", "Oracle"]
    auto_dialect = "SQL Server" if st.session_state.db_engine else "PostgreSQL"
    dialect = st.selectbox("SQL Dialect", dialect_options,
                           index=dialect_options.index(auto_dialect))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)

    st.divider()
    st.subheader("Data Source")
    data_source = st.radio("Connect via", ["CSV Upload", "Database"])

    # ── Database connection panel ─────────────────────────────────────────────
    if data_source == "Database":
        db_type = st.selectbox("Database Type",
                               ["SQL Server", "PostgreSQL", "MySQL", "SQLite"])

        if db_type == "SQLite":
            db_file = st.text_input("File Path", placeholder=r"C:\path\to\db.sqlite")
            db_host = db_port = db_user = db_pass = ""
            db_name = db_file
            windows_auth = False
        else:
            db_host = st.text_input("Host", value="localhost")
            db_port = st.text_input("Port", value=DEFAULT_PORTS.get(db_type, ""))
            db_name = st.text_input("Database Name")
            windows_auth = False
            if db_type == "SQL Server":
                windows_auth = st.checkbox("Windows Authentication (NTLM)", value=True)
            if not windows_auth:
                db_user = st.text_input("Username")
                db_pass = st.text_input("Password", type="password")
            else:
                db_user = db_pass = ""

        col_a, col_b = st.columns(2)
        with col_a:
            connect_btn = st.button("Connect", use_container_width=True, type="primary")
        with col_b:
            if st.button("Disconnect", use_container_width=True):
                st.session_state.db_engine = None
                st.session_state.db_tables = {}
                st.session_state.selected_table = None
                st.session_state.schema = ""
                st.rerun()

        if connect_btn:
            with st.spinner("Connecting..."):
                try:
                    url = build_url(db_type, db_host, db_port, db_name, db_user, db_pass, windows_auth)
                    engine = create_engine(url, connect_args={"connect_timeout": 5}
                                           if db_type not in ("SQLite", "SQL Server") else {})
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                    st.session_state.db_engine = engine
                    st.session_state.db_tables = load_db_tables(engine, db_type)
                    st.session_state.schema = tables_to_schema(st.session_state.db_tables)
                    st.session_state.selected_table = None
                    st.success(f"Connected — {len(st.session_state.db_tables)} table(s) found")
                    st.rerun()
                except Exception as e:
                    st.error(f"Connection failed:\n{str(e)[:250]}")

        # ── Table browser ─────────────────────────────────────────────────────
        if st.session_state.db_engine and st.session_state.db_tables:
            st.divider()
            st.markdown("**Tables**")
            for tbl in st.session_state.db_tables:
                col_count = len(st.session_state.db_tables[tbl])
                label = f"{'→ ' if st.session_state.selected_table == tbl else ''}{tbl} ({col_count} cols)"
                if st.button(label, key=f"tbl_{tbl}", use_container_width=True):
                    st.session_state.selected_table = tbl
                    st.rerun()

# ── Main area ─────────────────────────────────────────────────────────────────
db_connected = bool(st.session_state.db_engine)
selected_table = st.session_state.selected_table

# ── Table detail panel (when DB connected and table selected) ─────────────────
if db_connected and selected_table:
    st.subheader(f"Table: {selected_table}")
    cols_info = st.session_state.db_tables.get(selected_table, [])

    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.markdown("**Columns**")
        for c in cols_info:
            pk_badge = " 🔑" if c["pk"] else ""
            st.markdown(f"- `{c['name']}` — {c['type']}{pk_badge}")

    with col_right:
        st.markdown("**Preview (top 5 rows)**")
        try:
            with st.session_state.db_engine.connect() as conn:
                preview_df = pd.read_sql(text(f"SELECT TOP 5 * FROM {selected_table}"), conn)
            st.dataframe(preview_df, use_container_width=True)
        except Exception:
            try:
                with st.session_state.db_engine.connect() as conn:
                    preview_df = pd.read_sql(text(f"SELECT * FROM {selected_table} LIMIT 5"), conn)
                st.dataframe(preview_df, use_container_width=True)
            except Exception as e:
                st.caption(f"Preview unavailable: {e}")

    st.divider()

# ── Sample loader (CSV mode only) ─────────────────────────────────────────────
if not db_connected:
    with st.expander("💡 Load a Sample", expanded=False):
        selected_sample = st.selectbox("Choose a sample dataset",
                                       ["— select —"] + list(SAMPLES.keys()))
        if st.button("Load Sample", disabled=selected_sample == "— select —"):
            st.session_state.schema = SAMPLES[selected_sample]["schema"]
            st.session_state.query_request = SAMPLES[selected_sample]["query"]
            st.rerun()

# ── Schema (manual when CSV, auto when DB) ────────────────────────────────────
if not db_connected:
    with st.expander("Schema (optional)", expanded=False):
        st.text_area("Paste CREATE TABLE statements",
                     placeholder="CREATE TABLE ...",
                     height=180,
                     key="schema",
                     label_visibility="collapsed")

# ── Query Input ───────────────────────────────────────────────────────────────
if db_connected and selected_table:
    request_label = f"What do you want from **{selected_table}**?"
    placeholder = f"e.g. Show all rows where status is Active, sorted by date"
elif db_connected:
    request_label = "What do you want from your database?"
    placeholder = "e.g. Show all users and their roles"
else:
    request_label = "Describe what SQL you want to generate"
    placeholder = "e.g. Show the top 5 customers by total order value in the last 30 days"

st.subheader(request_label)
query_request = st.text_area("Request", placeholder=placeholder,
                              height=100, key="query_request",
                              label_visibility="collapsed")

# ── CSV upload ────────────────────────────────────────────────────────────────
uploaded_files = {}
if not db_connected and data_source == "CSV Upload":
    st.subheader("Upload CSV Data")
    st.caption("Filename becomes the table name")
    files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    for f in (files or []):
        tname = f.name.rsplit(".", 1)[0].replace(" ", "_").replace("-", "_")
        uploaded_files[tname] = pd.read_csv(f)
    if uploaded_files:
        st.success(f"Loaded: {', '.join(f'`{t}`' for t in uploaded_files)}")

# ── Buttons ───────────────────────────────────────────────────────────────────
def clear_form():
    st.session_state.query_request = ""
    if not db_connected:
        st.session_state.schema = ""

btn_label = "Fetch Data" if db_connected else "Generate SQL"
if not db_connected and uploaded_files:
    btn_label = "Generate & Run"

col1, col2, col3, _ = st.columns([1, 1, 1, 3])
with col1:
    go = st.button(btn_label, type="primary", use_container_width=True)
with col2:
    st.button("Clear", on_click=clear_form, use_container_width=True)
with col3:
    quick_fetch = (db_connected and selected_table and
                   st.button("Quick Fetch", use_container_width=True,
                             help="Instantly show all rows — no AI needed"))

# ── Quick Fetch (no LLM) ──────────────────────────────────────────────────────
if quick_fetch:
    st.subheader(f"Results — {selected_table} (all rows)")
    try:
        with st.session_state.db_engine.connect() as conn:
            result_df = pd.read_sql(text(f"SELECT * FROM {selected_table}"), conn)
        st.dataframe(result_df, use_container_width=True)
        st.caption(f"{len(result_df)} row(s)")
        st.download_button("⬇️ Download CSV", data=result_df.to_csv(index=False),
                           file_name=f"{selected_table}.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Fetch error: {e}")

# ── Execution ─────────────────────────────────────────────────────────────────
if go:
    if not query_request.strip():
        st.warning("Please describe what you want.")
        st.stop()

    # Build schema context for prompt
    if db_connected and selected_table:
        schema_ctx = selected_table_schema(selected_table, st.session_state.db_tables)
    elif db_connected:
        schema_ctx = tables_to_schema(st.session_state.db_tables)
    else:
        schema_ctx = st.session_state.schema

    schema_section = f"Database schema:\n{schema_ctx}\n\n" if schema_ctx.strip() else ""

    dialect_notes = {
        "SQL Server": "Use T-SQL syntax. Use YEAR(), MONTH(), DAY() instead of EXTRACT(). Use TOP N instead of LIMIT. Use GETDATE() instead of NOW().",
        "PostgreSQL": "Use PostgreSQL syntax. Use EXTRACT(), LIMIT, NOW().",
        "MySQL":      "Use MySQL syntax. Use YEAR(), MONTH(), LIMIT, NOW().",
        "SQLite":     "Use SQLite syntax. Use strftime() for dates, LIMIT.",
        "Oracle":     "Use Oracle SQL syntax. Use ROWNUM or FETCH FIRST N ROWS ONLY.",
    }
    dialect_hint = dialect_notes.get(dialect, "")

    prompt = f"""You are an expert {dialect} database administrator. Generate a clean, efficient SQL query.

{schema_section}User request: {query_request}

Rules:
- Output ONLY the SQL query, no explanation, no markdown
- Dialect: {dialect} — {dialect_hint}
- Format with proper indentation
- Use table aliases where helpful

SQL:"""

    try:
        # Stream SQL generation token by token
        sql_placeholder = st.empty()
        raw_sql = ""
        with st.spinner("Generating SQL..."):
            stream = ollama.chat(
                model=selected_model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": temperature},
                stream=True
            )
            for chunk in stream:
                token = chunk.message.content
                raw_sql += token
                # Show live preview stripped of fences
                preview = raw_sql.strip().lstrip("```sql").lstrip("```").strip()
                sql_placeholder.code(preview or "...", language="sql")

        if raw_sql.startswith("```"):
            lines = raw_sql.split("\n")
            raw_sql = "\n".join(l for l in lines if not l.strip().startswith("```")).strip()

        formatted_sql = sqlparse.format(
            raw_sql, reindent=True, keyword_case="upper",
            identifier_case="lower", strip_comments=False
        )
        sql_placeholder.empty()

        # ── Show results if DB connected ──────────────────────────────────
        if db_connected:
            st.subheader("Results")
            try:
                with st.session_state.db_engine.connect() as conn:
                    result_df = pd.read_sql(text(formatted_sql), conn)
                st.dataframe(result_df, use_container_width=True)
                st.caption(f"{len(result_df)} row(s) returned")
                st.download_button("⬇️ Download CSV",
                                   data=result_df.to_csv(index=False),
                                   file_name="results.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Query error: {e}")

            with st.expander("View generated SQL"):
                st.code(formatted_sql, language="sql")
                escaped = html.escape(formatted_sql, quote=True)
                components.html(f"""
                    <button id="cb" onclick="
                        navigator.clipboard.writeText(document.getElementById('st').value)
                            .then(()=>{{document.getElementById('cb').textContent='Copied!';
                            setTimeout(()=>document.getElementById('cb').textContent='Copy SQL',2000)}})
                    " style="background:#4CAF50;color:white;border:none;padding:6px 14px;
                             border-radius:5px;cursor:pointer;font-size:13px;font-weight:600">
                        Copy SQL
                    </button>
                    <textarea id="st" style="display:none">{escaped}</textarea>
                """, height=40)

        # ── CSV / SQL-only mode ───────────────────────────────────────────
        else:
            st.subheader("Generated SQL")
            st.code(formatted_sql, language="sql")

            col_copy, col_dl, _ = st.columns([1, 1, 4])
            with col_copy:
                escaped = html.escape(formatted_sql, quote=True)
                components.html(f"""
                    <button id="copybtn" onclick="
                        navigator.clipboard.writeText(document.getElementById('sqltext').value)
                            .then(()=>{{document.getElementById('copybtn').textContent='Copied!';
                            setTimeout(()=>document.getElementById('copybtn').textContent='Copy SQL',2000)}})
                    " style="background:#4CAF50;color:white;border:none;padding:8px 18px;
                             border-radius:6px;cursor:pointer;font-size:14px;font-weight:600;width:100%">
                        Copy SQL
                    </button>
                    <textarea id="sqltext" style="display:none">{escaped}</textarea>
                """, height=45)
            with col_dl:
                st.download_button("⬇️ Download .sql", data=formatted_sql,
                                   file_name="query.sql", mime="text/plain",
                                   use_container_width=True)

            if uploaded_files:
                st.subheader("Results")
                try:
                    con = duckdb.connect()
                    for tname, df in uploaded_files.items():
                        con.register(tname, df)
                    result_df = con.execute(formatted_sql).df()
                    st.dataframe(result_df, use_container_width=True)
                    st.caption(f"{len(result_df)} row(s) returned")
                    st.download_button("⬇️ Download Results CSV",
                                       data=result_df.to_csv(index=False),
                                       file_name="results.csv", mime="text/csv")
                except Exception as e:
                    st.error(f"Query error: {e}")
                finally:
                    con.close()

        # Store history
        st.session_state.history.insert(0, {
            "request": query_request,
            "sql": formatted_sql,
            "model": selected_model,
            "dialect": dialect,
            "table": selected_table or "—"
        })

    except ollama.ResponseError as e:
        st.error(f"Ollama error: {e.error}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    st.subheader("Session History")
    for i, entry in enumerate(st.session_state.history[:10]):
        label = f"{i+1}. [{entry['table']}] {entry['request'][:70]}{'...' if len(entry['request'])>70 else ''}"
        with st.expander(label):
            st.caption(f"Model: `{entry['model']}` | Dialect: `{entry['dialect']}`")
            st.code(entry["sql"], language="sql")
