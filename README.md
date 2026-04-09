# expense_tracker
# 💰 Expense Tracker

A professional Python CLI application to track daily expenses with CSV storage, summaries, and graph visualizations. Built with clean architecture and suitable for portfolio / resume use.



## 📁 Folder Structure


expense_tracker/
├── expense_tracker.py   # Main entry point — menu & flow control
├── data_manager.py      # CSV CRUD layer (add/edit/delete/search)
├── validator.py         # Input validation (amount, date, category)
├── visualizer.py        # Matplotlib charts (pie, bar, line, dashboard)
├── reports.py           # Category & monthly summaries + TXT export
├── config.py            # Central config (paths, categories, constants)
├── requirements.txt     # Dependencies
├── data/
│   └── expenses.csv     # Auto-created — all expense records
└── reports/
    ├── pie_chart.png    # Category pie chart
    ├── bar_monthly.png  # Monthly bar chart
    ├── line_trend.png   # Daily trend line chart
    ├── dashboard.png    # 4-panel combined dashboard
    └── *.txt            # Exported text reports




## 🚀 Setup & Run

bash
# 1. Clone / download the project
cd expense_tracker

# 2. Install dependency
pip install matplotlib

# 3. Run
python expense_tracker.py


---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add Expense | Description, amount, category (12 types), date |
| ✏️ Edit Expense | Update any field of an existing record |
| 🗑️ Delete Expense | Remove with confirmation prompt |
| 📋 View All | Tabular view with total |
| 🔍 Search | Filter by keyword (description or category) |
| 📊 Category Summary | Sorted totals with % share + ASCII bar |
| 📅 Monthly Summary | Month-by-month breakdown by category |
| 📈 Graphs | Pie, bar, line, dashboard (all dark-themed) |
| 📤 Export | Full text report saved with timestamp |
| ✅ Validation | Amount, date format, category, ID checks |

---

## 🔑 Architecture Notes

- **Separation of concerns** — each file has a single responsibility
- **DataManager** abstracts all CSV I/O; easy to swap with SQLite
- **Validator** is pure functions — no side effects, easy to unit test
- **Config** is the single source of truth for categories and paths
- **Visualizer** is stateless — pass any list of records, get a chart

---

