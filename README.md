# ChatLLaMA (Gemini Text-to-SQL + MySQL + Local LLaMA Summarization)

A production-style FastAPI backend that answers natural-language questions using a MySQL database.

**How it works (high level):**
1. **Gemini** generates a **MySQL SELECT query** (JSON output).
2. Backend applies **strict SQL security validation** (SELECT-only, allowlisted tables, LIMIT enforcement, password blocking, etc.).
3. Backend executes the query on **MySQL** (read-only recommended).
4. **Local LLaMA (Ollama)** converts the raw rows into a **human conversational Markdown answer**.

This design improves speed and reliability compared to agent-based approaches while keeping the final response generation **local**.

---

## Features

- Natural language → SQL using **Gemini**
- Safe SQL execution on **MySQL**
- Local response generation using **Ollama (LLaMA 3.x / 3.2)**
- Output in **Markdown**, conversational format (no tables for single-row answers)
- Fast and stable architecture (no ReAct tool loops required)
- Strong security guardrails for LLM-generated SQL

---

## Tech Stack

- **FastAPI** (backend)
- **MySQL** (database)
- **SQLAlchemy** (DB execution)
- **Gemini API** (Text-to-SQL generation)
- **Ollama** (local LLaMA inference)
- **LangChain Community** (Ollama wrapper, optional)

---

## Project Structure

