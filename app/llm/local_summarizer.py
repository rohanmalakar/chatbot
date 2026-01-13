from langchain_community.llms import Ollama
from app.core.config import settings

STATUS_MAP = {
    0: "Active",
    1: "Inactive",
}

def summarize(question: str, sql: str, rows: list[dict]) -> str:
    llm = Ollama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.5,  # keep deterministic
    )

    # Truncate for safety
    rows = rows[:20]

    # Pre-normalize common fields for better output
    def normalize_row(r: dict) -> dict:
        rr = dict(r)
        if "estatus" in rr:
            try:
                rr["estatus_text"] = STATUS_MAP.get(int(rr["estatus"]), str(rr["estatus"]))
            except Exception:
                rr["estatus_text"] = str(rr["estatus"])
        return rr

    norm_rows = [normalize_row(r) for r in rows]

    prompt = f"""
You are a conversational assistant.

OUTPUT RULES (STRICT):
- Output MUST be Markdown only.
- Do NOT output any tables.
- Do NOT output JSON.
- Do NOT say filler phrases like: "Let me take a look", "Here are the details", "It seems like".
- Do NOT mention SQL, database, LIMIT, truncation, or "query".
- Keep it short and natural.

FORMATTING RULES:
- If there is exactly 1 row: write 2–4 short lines, using bullets only if helpful.
- If there are multiple rows: write 1–2 line summary and then a short bullet list (no tables).

DATA:
User question: {question}

Rows (JSON):
{norm_rows}

SPECIAL FIELD RULE:
- If 'estatus_text' exists, use it as the status (ignore numeric 'estatus').

Now produce the final answer.
"""

    return llm.invoke(prompt).strip()
