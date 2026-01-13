# app/llm/schema.py

SCHEMA_DESCRIPTION = """
Database: app_db (MySQL)

Table: events
- event_id (int)
- ename (varchar)
- event_start (datetime)
- event_end (datetime)
- category (varchar)
- estatus (varchar)
- disciplines (varchar)
- school_participants (int)
- user_participants (int)
- eimage (longtext)
- etype (varchar)
- emonitored (varchar)

Table: users
- id (int)
- fname (varchar)
- lname (varchar)
- gender (varchar)
- email (varchar)
- mobile (varchar)
- dob (date)
- age (int)
- address (varchar)
- city (varchar)
- state (varchar)
- pincode (varchar)
- country (varchar)
- school_name (varchar)
- school_class (varchar)
- membership_type (varchar)
- password (varchar)
- image (longtext)
- created_date (timestamp)
- created_by (varchar)
- uid (varchar)
- cat_id (int)
- category_name (varchar)
- name (varchar)

Rules:
- Use MySQL syntax only
- Use only these two tables and listed columns
- Never query or return password unless explicitly asked (prefer not returning it)
- Always use LIMIT <= 100
"""

ALLOWED_TABLES = {"events", "users"}
