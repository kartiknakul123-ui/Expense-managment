"""SQLite database layer for the Expense Management System."""
from pathlib import Path
import sqlite3
from datetime import date

DB_PATH = Path(__file__).resolve().with_name("expenses.db")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                expense_date TEXT NOT NULL,
                payment_method TEXT NOT NULL DEFAULT 'Cash',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = con.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        if count == 0:
            con.executemany("""
                INSERT INTO expenses(title, category, amount, expense_date, payment_method, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                ("Lunch", "Food", 180.00, date.today().isoformat(), "UPI", "Sample record"),
                ("Bus fare", "Travel", 60.00, date.today().isoformat(), "Cash", "Sample record"),
                ("Notebook", "Education", 95.00, date.today().isoformat(), "Cash", "Sample record"),
            ])

def add_expense(title, category, amount, expense_date, payment_method, notes):
    with connect() as con:
        con.execute("""
            INSERT INTO expenses(title, category, amount, expense_date, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title.strip(), category, float(amount), expense_date, payment_method, notes.strip()))

def get_expenses(search=""):
    with connect() as con:
        term = f"%{search.strip()}%"
        return con.execute("""
            SELECT * FROM expenses
            WHERE title LIKE ? OR category LIKE ? OR payment_method LIKE ? OR notes LIKE ?
            ORDER BY expense_date DESC, id DESC
        """, (term, term, term, term)).fetchall()

def delete_expense(expense_id):
    with connect() as con:
        con.execute("DELETE FROM expenses WHERE id = ?", (int(expense_id),))

def get_summary():
    with connect() as con:
        total = con.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        count = con.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        today_total = con.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE expense_date = date('now','localtime')"
        ).fetchone()[0]
        month_total = con.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM expenses
            WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now', 'localtime')
        """).fetchone()[0]
        categories = con.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses GROUP BY category ORDER BY total DESC
        """).fetchall()
        return {"total": total, "count": count, "today": today_total,
                "month": month_total, "categories": categories}

def export_rows():
    with connect() as con:
        return con.execute("""
            SELECT id, title, category, amount, expense_date, payment_method, notes
            FROM expenses ORDER BY expense_date DESC, id DESC
        """).fetchall()
