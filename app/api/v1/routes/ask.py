from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.llm.gemini_sql import generate_sql
from app.llm.sql_guard import validate_sql
from app.llm.local_summarizer import summarize

router = APIRouter(prefix="/ask", tags=["Ask"])

class AskRequest(BaseModel):
    question: str

@router.post("")
def ask(payload: AskRequest, db: Session = Depends(get_db)):
    try:
        # 1) Gemini generates SQL
        data = generate_sql(payload.question)
        sql = data.get("sql", "")

        if not sql:
            return {"answer": "I cannot answer that using the available schema.", "sql": ""}

        # 2) Validate SQL (critical)
        safe_sql = validate_sql(sql)

        # 3) Execute SQL
        result = db.execute(text(safe_sql))
        cols = result.keys()
        rows = [dict(zip(cols, r)) for r in result.fetchall()]

        # 4) Summarize locally (keep small for speed)
        answer = summarize(payload.question, safe_sql, rows[:30])

        return {"answer": answer, "sql": safe_sql, "rows": rows[:30]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
