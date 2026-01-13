# app/llm/gemini_sql.py
import json
from google import genai

from app.core.config import settings
from app.llm.schema import SCHEMA_DESCRIPTION

# Recommended fast model for SQL generation
MODEL_NAME = "models/gemini-flash-lite-latest"
# Alternatives:
# MODEL_NAME = "models/gemini-flash-latest"
# MODEL_NAME = "models/gemini-2.5-pro"

SYSTEM_PROMPT = f"""
You are a STRICT MySQL Text-to-SQL generator.

Return ONLY valid JSON. No markdown. No explanations.

Output JSON format (MUST match exactly):
{{
  "sql": "<single MySQL SELECT query ending with LIMIT N>",
  "tables": ["<table1>", "<table2>"],
  "limit": <integer N between 1 and 100>
}}

HARD RULES:
1) SQL must be SELECT-only. Never use INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/CREATE/GRANT/REVOKE.
2) Always include LIMIT N at the end of the SQL. N must equal the JSON 'limit'.
3) N must be between 1 and 100.
4) For aggregate queries (COUNT, SUM, AVG, MIN, MAX):
   - ALWAYS use an alias with AS, e.g.:
     SELECT COUNT(id) AS total_users FROM users LIMIT 1
5) Use ONLY the tables/columns listed in the schema. Do not invent columns.
6) If the request cannot be answered from the schema, return:
   {{ "sql": "", "tables": [], "limit": 0 }}

Schema:
{SCHEMA_DESCRIPTION}

Examples:
User: "How many users are there?"
Return:
{{"sql":"SELECT COUNT(u.id) AS total_users FROM users u LIMIT 1","tables":["users"],"limit":1}}

User: "List 10 latest events"
Return:
{{"sql":"SELECT e.event_id, e.ename, e.event_start FROM events e ORDER BY e.event_start DESC LIMIT 10","tables":["events"],"limit":10}}
"""


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_sql(question: str) -> dict:
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0,
        },
    )
    
    text = (resp.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned empty response text")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # fallback extraction if extra text appears
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end + 1])
        raise RuntimeError(f"Gemini did not return valid JSON. Raw output: {text}")
