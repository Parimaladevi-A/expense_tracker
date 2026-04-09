"""
Expense Tracker - Main Application
A professional CLI-based expense tracker with CSV storage and graph visualization.
"""

import csv
import os
import sys
from datetime import datetime
from typing import Optional

from data_manager import DataManager
from validator import validate_amount, validate_date, validate_category
from visualizer import ExpenseVisualizer
from reports import ReportGenerator
from config import CATEGORIES, CSV_FILE, DATE_FORMAT


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("\n" + "=" * 55)
    print("          💰  EXPENSE TRACKER  💰")
    print("=" * 55)


def print_menu():
    print_header()
    print("  1. ➕  Add Expense")
    print("  2. 📋  View All Expenses")
    print("  3. ✏️   Edit Expense")
    print("  4. 🗑️   Delete Expense")
    print("  5. 📊  Category Summary")
    print("  6. 📅  Monthly Summary")
    print("  7. 📈  View Graphs")
    print("  8. 🔍  Search Expenses")
    print("  9. 📤  Export Report")
    print("  0. 🚪  Exit")
    print("-" * 55)


def get_input(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  ⚠️  Input cannot be empty. Please try again.")


def display_categories():
    print("\n  Available Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")


def add_expense(dm: DataManager):
    print("\n--- Add New Expense ---")
    description = get_input("  Description: ")

    while True:
        raw_amount = get_input("  Amount (₹): ")
        amount = validate_amount(raw_amount)
        if amount is not None:
            break
        print("  ⚠️  Invalid amount. Enter a positive number (e.g. 250.50).")

    display_categories()
    while True:
        cat_input = get_input("  Category (number or name): ")
        category = validate_category(cat_input, CATEGORIES)
        if category:
            break
        print(f"  ⚠️  Invalid category. Choose from list or enter number 1-{len(CATEGORIES)}.")

    while True:
        date_input = get_input(f"  Date [{DATE_FORMAT}] (press Enter for today): ", allow_empty=True)
        if not date_input:
            date_input = datetime.today().strftime(DATE_FORMAT)
        date = validate_date(date_input)
        if date:
            break
        print(f"  ⚠️  Invalid date. Use format {DATE_FORMAT} (e.g. 2024-07-15).")

    expense = {
        "id": dm.next_id(),
        "date": date,
        "description": description,
        "category": category,
        "amount": round(amount, 2),
    }

    dm.add(expense)
    print(f"\n  ✅ Expense added successfully! (ID: {expense['id']})")


def view_expenses(dm: DataManager, expenses: Optional[list] = None, title: str = "All Expenses"):
    data = expenses if expenses is not None else dm.all()
    if not data:
        print("\n  📭 No expenses found.")
        return

    print(f"\n--- {title} ({len(data)} records) ---")
    print(f"  {'ID':<5} {'Date':<12} {'Category':<18} {'Amount':>10}  {'Description'}")
    print("  " + "-" * 65)
    total = 0.0
    for e in data:
        print(f"  {e['id']:<5} {e['date']:<12} {e['category']:<18} ₹{float(e['amount']):>9,.2f}  {e['description']}")
        total += float(e["amount"])
    print("  " + "-" * 65)
    print(f"  {'TOTAL':<36} ₹{total:>9,.2f}")


def edit_expense(dm: DataManager):
    view_expenses(dm)
    if not dm.all():
        return

    while True:
        id_input = get_input("\n  Enter Expense ID to edit (or 0 to cancel): ")
        if id_input == "0":
            return
        expense = dm.find_by_id(id_input)
        if expense:
            break
        print("  ⚠️  Expense not found. Try again.")

    print(f"\n  Editing: [{expense['id']}] {expense['description']} | {expense['category']} | ₹{expense['amount']} | {expense['date']}")
    print("  (Press Enter to keep current value)\n")

    new_desc = input(f"  Description [{expense['description']}]: ").strip() or expense["description"]

    while True:
        raw = input(f"  Amount [{expense['amount']}]: ").strip()
        if not raw:
            new_amount = float(expense["amount"])
            break
        new_amount = validate_amount(raw)
        if new_amount is not None:
            break
        print("  ⚠️  Invalid amount.")

    display_categories()
    while True:
        raw_cat = input(f"  Category [{expense['category']}]: ").strip()
        if not raw_cat:
            new_cat = expense["category"]
            break
        new_cat = validate_category(raw_cat, CATEGORIES)
        if new_cat:
            break
        print("  ⚠️  Invalid category.")

    while True:
        raw_date = input(f"  Date [{expense['date']}]: ").strip()
        if not raw_date:
            new_date = expense["date"]
            break
        new_date = validate_date(raw_date)
        if new_date:
            break
        print(f"  ⚠️  Invalid date. Use {DATE_FORMAT}.")

    updated = {
        "id": expense["id"],
        "date": new_date,
        "description": new_desc,
        "category": new_cat,
        "amount": round(new_amount, 2),
    }
    dm.update(expense["id"], updated)
    print("\n  ✅ Expense updated successfully!")


def delete_expense(dm: DataManager):
    view_expenses(dm)
    if not dm.all():
        return

    while True:
        id_input = get_input("\n  Enter Expense ID to delete (or 0 to cancel): ")
        if id_input == "0":
            return
        expense = dm.find_by_id(id_input)
        if expense:
            break
        print("  ⚠️  Expense not found.")

    confirm = input(f"  ⚠️  Delete [{expense['id']}] '{expense['description']}' ₹{expense['amount']}? (yes/no): ").strip().lower()
    if confirm == "yes":
        dm.delete(expense["id"])
        print("  ✅ Expense deleted.")
    else:
        print("  ❌ Deletion cancelled.")


def search_expenses(dm: DataManager):
    print("\n--- Search Expenses ---")
    keyword = get_input("  Enter keyword (description/category): ").lower()
    results = [
        e for e in dm.all()
        if keyword in e["description"].lower() or keyword in e["category"].lower()
    ]
    view_expenses(dm, results, title=f"Search: '{keyword}'")


def graphs_menu(viz: ExpenseVisualizer, dm: DataManager):
    if not dm.all():
        print("\n  📭 No data to visualize.")
        return
    print("\n--- Graph Options ---")
    print("  1. Pie Chart - Spending by Category")
    print("  2. Bar Chart - Monthly Spending")
    print("  3. Line Chart - Daily Spending Trend")
    print("  4. All Charts (Dashboard)")
    choice = get_input("  Choose: ")
    data = dm.all()
    if choice == "1":
        viz.pie_chart(data)
    elif choice == "2":
        viz.bar_chart_monthly(data)
    elif choice == "3":
        viz.line_chart_trend(data)
    elif choice == "4":
        viz.dashboard(data)
    else:
        print("  ⚠️  Invalid choice.")


def main():
    dm = DataManager(CSV_FILE)
    viz = ExpenseVisualizer()
    reporter = ReportGenerator()

    while True:
        clear_screen()
        print_menu()
        choice = input("  Select option: ").strip()

        if choice == "1":
            add_expense(dm)
        elif choice == "2":
            view_expenses(dm)
        elif choice == "3":
            edit_expense(dm)
        elif choice == "4":
            delete_expense(dm)
        elif choice == "5":
            reporter.category_summary(dm.all())
        elif choice == "6":
            reporter.monthly_summary(dm.all())
        elif choice == "7":
            graphs_menu(viz, dm)
        elif choice == "8":
            search_expenses(dm)
        elif choice == "9":
            reporter.export_txt(dm.all())
        elif choice == "0":
            print("\n  👋 Goodbye! Track your expenses wisely.\n")
            sys.exit(0)
        else:
            print("  ⚠️  Invalid option.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
