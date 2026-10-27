"""Expense Management System - Python, Tkinter and SQLite."""
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import database

BG = "#f3f6fb"
NAVY = "#183153"
BLUE = "#2878d0"
GREEN = "#198754"

class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        database.init_db()
        self.title("Expense Management System")
        self.geometry("1100x720")
        self.minsize(950, 620)
        self.configure(bg=BG)
        self.selected_id = None
        self._style()
        self._build()
        self.refresh_all()

    def _style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#e5edf7", foreground=NAVY)
        style.configure("TNotebook.Tab", padding=(16, 9), font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=BG, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=7)

    def _build(self):
        header = tk.Frame(self, bg=NAVY, padx=22, pady=17)
        header.pack(fill="x")
        tk.Label(header, text="EXPENSE MANAGEMENT SYSTEM", bg=NAVY, fg="white",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w")
        tk.Label(header, text="Record spending • Review summaries • Stay on budget",
                 bg=NAVY, fg="#d9e7f8", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=16)
        self.dashboard_tab = tk.Frame(self.tabs, bg=BG, padx=16, pady=16)
        self.expense_tab = tk.Frame(self.tabs, bg=BG, padx=16, pady=16)
        self.reports_tab = tk.Frame(self.tabs, bg=BG, padx=16, pady=16)
        self.tabs.add(self.dashboard_tab, text="Dashboard")
        self.tabs.add(self.expense_tab, text="Expenses")
        self.tabs.add(self.reports_tab, text="Reports")
        self._build_dashboard()
        self._build_expenses()
        self._build_reports()

    def _card(self, parent, title, variable, color):
        frame = tk.Frame(parent, bg="white", padx=18, pady=15,
                         highlightbackground="#dce4ef", highlightthickness=1)
        tk.Label(frame, text=title, bg="white", fg="#526277",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(frame, textvariable=variable, bg="white", fg=color,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(8, 0))
        return frame

    def _build_dashboard(self):
        tk.Label(self.dashboard_tab, text="Your spending at a glance", bg=BG, fg=NAVY,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))
        cards = tk.Frame(self.dashboard_tab, bg=BG)
        cards.pack(fill="x")
        self.total_var = tk.StringVar(value="₹0.00")
        self.month_var = tk.StringVar(value="₹0.00")
        self.today_var = tk.StringVar(value="₹0.00")
        self.count_var = tk.StringVar(value="0")
        for title, var, color in [
            ("TOTAL EXPENSES", self.total_var, BLUE),
            ("THIS MONTH", self.month_var, GREEN),
            ("TODAY", self.today_var, "#b76e00"),
            ("RECORDS", self.count_var, NAVY)
        ]:
            self._card(cards, title, var, color).pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(self.dashboard_tab, text="Category-wise spending", bg=BG, fg=NAVY,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(25, 9))
        self.category_tree = ttk.Treeview(self.dashboard_tab, columns=("category", "amount"),
                                          show="headings", height=9)
        self.category_tree.heading("category", text="Category")
        self.category_tree.heading("amount", text="Total Spent (₹)")
        self.category_tree.column("category", width=420)
        self.category_tree.column("amount", width=220, anchor="e")
        self.category_tree.pack(fill="both", expand=True)

    def _build_expenses(self):
        tk.Label(self.expense_tab, text="Add and manage expenses", bg=BG, fg=NAVY,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))
        form = tk.Frame(self.expense_tab, bg="white", padx=14, pady=12,
                        highlightbackground="#dce4ef", highlightthickness=1)
        form.pack(fill="x")
        self.title_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Food")
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.payment_var = tk.StringVar(value="UPI")
        self.notes_var = tk.StringVar()
        fields = [
            ("Expense title", self.title_var, 0, 0),
            ("Amount (₹)", self.amount_var, 0, 2),
            ("Date (YYYY-MM-DD)", self.date_var, 1, 0),
            ("Notes (optional)", self.notes_var, 1, 2),
        ]
        for label, var, r, c in fields:
            tk.Label(form, text=label, bg="white", fg="#35465c").grid(row=r, column=c, sticky="w", padx=5, pady=4)
            tk.Entry(form, textvariable=var, width=29, font=("Segoe UI", 10)).grid(
                row=r, column=c+1, sticky="ew", padx=5, pady=4, ipady=4)
        tk.Label(form, text="Category", bg="white", fg="#35465c").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Combobox(form, textvariable=self.category_var, state="readonly", width=26,
                     values=["Food", "Travel", "Education", "Shopping", "Bills", "Health", "Entertainment", "Other"]).grid(
                         row=2, column=1, sticky="ew", padx=5, pady=4)
        tk.Label(form, text="Payment method", bg="white", fg="#35465c").grid(row=2, column=2, sticky="w", padx=5, pady=4)
        ttk.Combobox(form, textvariable=self.payment_var, state="readonly", width=26,
                     values=["Cash", "UPI", "Debit Card", "Credit Card", "Net Banking", "Other"]).grid(
                         row=2, column=3, sticky="ew", padx=5, pady=4)
        for c in range(4):
            form.grid_columnconfigure(c, weight=1)
        actions = tk.Frame(form, bg="white")
        actions.grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))
        ttk.Button(actions, text="Add Expense", command=self.add_expense).pack(side="left", padx=4)
        ttk.Button(actions, text="Clear Form", command=self.clear_form).pack(side="left", padx=4)
        ttk.Button(actions, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=4)
        ttk.Button(actions, text="Export CSV", command=self.export_csv).pack(side="left", padx=4)

        searchrow = tk.Frame(self.expense_tab, bg=BG)
        searchrow.pack(fill="x", pady=(15, 7))
        tk.Label(searchrow, text="Search:", bg=BG, fg=NAVY, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(searchrow, textvariable=self.search_var, width=34, font=("Segoe UI", 10))
        search_entry.pack(side="left", padx=8, ipady=4)
        ttk.Button(searchrow, text="Search", command=self.refresh_expenses).pack(side="left", padx=3)
        ttk.Button(searchrow, text="Show All", command=self.show_all).pack(side="left", padx=3)

        columns = ("id", "title", "category", "amount", "date", "payment", "notes")
        self.expense_tree = ttk.Treeview(self.expense_tab, columns=columns, show="headings", height=10)
        labels = {"id":"ID", "title":"Expense", "category":"Category", "amount":"Amount (₹)",
                  "date":"Date", "payment":"Payment", "notes":"Notes"}
        widths = {"id":45, "title":170, "category":120, "amount":110, "date":105, "payment":115, "notes":190}
        for col in columns:
            self.expense_tree.heading(col, text=labels[col])
            self.expense_tree.column(col, width=widths[col], anchor="e" if col=="amount" else "w")
        self.expense_tree.pack(fill="both", expand=True)
        self.expense_tree.bind("<<TreeviewSelect>>", self.on_select)

    def _build_reports(self):
        tk.Label(self.reports_tab, text="Expense report", bg=BG, fg=NAVY,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 8))
        tk.Label(self.reports_tab, text="Use Export CSV on the Expenses tab to save all records for a spreadsheet or submission.",
                 bg=BG, fg="#526277", wraplength=850, justify="left").pack(anchor="w", pady=(0, 16))
        self.report_summary = tk.StringVar()
        tk.Label(self.reports_tab, textvariable=self.report_summary, bg="white", fg=NAVY,
                 font=("Segoe UI", 12), justify="left", padx=20, pady=20,
                 anchor="nw", relief="solid", bd=1).pack(fill="both", expand=True)

    def add_expense(self):
        title = self.title_var.get().strip()
        amount_text = self.amount_var.get().strip()
        expense_date = self.date_var.get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please enter an expense title.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid amount", "Amount must be a number greater than zero.")
            return
        try:
            date.fromisoformat(expense_date)
        except ValueError:
            messagebox.showwarning("Invalid date", "Enter date in YYYY-MM-DD format.")
            return
        database.add_expense(title, self.category_var.get(), amount, expense_date,
                             self.payment_var.get(), self.notes_var.get())
        self.clear_form()
        self.refresh_all()
        messagebox.showinfo("Saved", "Expense added successfully.")

    def clear_form(self):
        self.title_var.set("")
        self.amount_var.set("")
        self.date_var.set(date.today().isoformat())
        self.notes_var.set("")
        self.category_var.set("Food")
        self.payment_var.set("UPI")
        self.selected_id = None
        if hasattr(self, "expense_tree"):
            self.expense_tree.selection_remove(self.expense_tree.selection())

    def on_select(self, _event=None):
        selected = self.expense_tree.selection()
        if selected:
            values = self.expense_tree.item(selected[0], "values")
            self.selected_id = int(values[0])

    def delete_selected(self):
        selected = self.expense_tree.selection()
        if not selected:
            messagebox.showwarning("Select a record", "Please select an expense row first.")
            return
        values = self.expense_tree.item(selected[0], "values")
        if messagebox.askyesno("Confirm delete", f"Delete expense '{values[1]}'?"):
            database.delete_expense(values[0])
            self.clear_form()
            self.refresh_all()

    def refresh_expenses(self):
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        for row in database.get_expenses(self.search_var.get()):
            self.expense_tree.insert("", "end", values=(
                row["id"], row["title"], row["category"], f'{row["amount"]:.2f}',
                row["expense_date"], row["payment_method"], row["notes"]))

    def show_all(self):
        self.search_var.set("")
        self.refresh_expenses()

    def refresh_all(self):
        summary = database.get_summary()
        self.total_var.set(f'₹{summary["total"]:,.2f}')
        self.month_var.set(f'₹{summary["month"]:,.2f}')
        self.today_var.set(f'₹{summary["today"]:,.2f}')
        self.count_var.set(str(summary["count"]))
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        for row in summary["categories"]:
            self.category_tree.insert("", "end", values=(row["category"], f'{row["total"]:,.2f}'))
        self.refresh_expenses()
        lines = [
            "EXPENSE SUMMARY",
            "",
            f'Total amount recorded: ₹{summary["total"]:,.2f}',
            f'Amount spent today: ₹{summary["today"]:,.2f}',
            f'Amount spent this month: ₹{summary["month"]:,.2f}',
            f'Total expense records: {summary["count"]}',
            "",
            "CATEGORY BREAKDOWN",
        ]
        lines += [f'• {row["category"]}: ₹{row["total"]:,.2f}' for row in summary["categories"]]
        self.report_summary.set("\n".join(lines))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export expenses", defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")], initialfile="expense_report.csv")
        if not path:
            return
        rows = database.export_rows()
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Category", "Amount", "Date", "Payment Method", "Notes"])
            for row in rows:
                writer.writerow([row["id"], row["title"], row["category"], row["amount"],
                                 row["expense_date"], row["payment_method"], row["notes"]])
        messagebox.showinfo("Export complete", f"Saved {len(rows)} records to:\n{path}")

if __name__ == "__main__":
    ExpenseApp().mainloop()
