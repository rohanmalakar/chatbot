import re
from app.llm.schema import ALLOWED_TABLES

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|grant|revoke|create|replace)\b",
    re.IGNORECASE
)

def validate_sql(sql: str, max_limit: int = 100) -> str:
    if not sql or not sql.strip():
        raise ValueError("Empty SQL generated")

    s = sql.strip()

    # no multi-statement
    if ";" in s:
        raise ValueError("Multiple statements not allowed")

    # must start with SELECT
    if not re.match(r"^\s*select\b", s, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed")

    # forbid destructive keywords
    if FORBIDDEN.search(s):
        raise ValueError("Forbidden SQL operation detected")

    # block password selection (extra safety)
    if re.search(r"\busers\.password\b|\bpassword\b", s, re.IGNORECASE):
        raise ValueError("Selecting password is blocked")

    # allowlist tables (FROM / JOIN)
    tables = re.findall(r"\bfrom\s+([a-zA-Z_][\w]*)|\bjoin\s+([a-zA-Z_][\w]*)", s, re.IGNORECASE)
    used = set()
    for a, b in tables:
        if a: used.add(a.lower())
        if b: used.add(b.lower())

    unknown = [t for t in used if t not in {x.lower() for x in ALLOWED_TABLES}]
    if unknown:
        raise ValueError(f"Non-allowed tables referenced: {unknown}")

    # enforce LIMIT
    if not re.search(r"\blimit\b", s, re.IGNORECASE):
        s = s + f" LIMIT {max_limit}"
    else:
        m = re.search(r"\blimit\s+(\d+)\b", s, re.IGNORECASE)
        if m and int(m.group(1)) > max_limit:
            s = re.sub(r"\blimit\s+\d+\b", f"LIMIT {max_limit}", s, flags=re.IGNORECASE)

    return s
