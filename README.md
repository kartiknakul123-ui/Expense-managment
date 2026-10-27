# Expense Management System (Python + Tkinter + SQLite)

## Features
- Dashboard showing total expenses, this month's spending, today's spending, and record count
- Add expense with title, category, amount, date, payment method, and notes
- Search expense records
- Delete selected records with confirmation
- Category-wise spending summary
- Export all expenses to CSV
- SQLite storage; data remains saved after closing the application
- Input validation for positive amounts and YYYY-MM-DD dates

## Requirements
- Python 3.10 or newer recommended
- Tkinter (included with most Windows Python installations)
- SQLite (included with Python's `sqlite3` module)
- No third-party packages required

## Run on Windows
1. Extract this folder.
2. Open the folder in VS Code or Command Prompt.
3. Run `python main.py` (or `py main.py`).
4. The `expenses.db` database is created automatically.

## Files
- `main.py`: Tkinter interface and application logic
- `database.py`: SQLite queries and summary calculations
- `sample_expenses.csv`: example data in spreadsheet format
- `requirements.txt`: notes that no external packages are required
- `Expense_Management_System_Report.docx`: project report

## How to use
1. Open the Dashboard to see spending summaries.
2. Go to Expenses and fill the form, then click Add Expense.
3. Use Search to find records by title, category, payment method, or notes.
4. Select a row and click Delete Selected to remove it.
5. Click Export CSV to save records for Excel or further analysis.

## Project explanation (Hinglish)
- `main.py`: Tkinter se window, forms, buttons aur tables bante hain. User yahin se expense add/search/delete karta hai.
- `database.py`: SQLite database banata hai aur expense records, total spending aur category-wise calculations handle karta hai.
- `expenses.db`: Data file hai. App band karne ke baad bhi records saved rehte hain.
- `expenses` table mein title, category, amount, date, payment method aur notes store hote hain.
- Total expenses = sabhi saved expense amounts ka sum.
- Category-wise report har category ka total spending dikhati hai.
