from typing import Any
import click
import json
from datetime import datetime
import os
import prettytable
from prettytable.prettytable import PrettyTable


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses: list[dict[str, Any]] = []
        self.next_id = 1
        self.load_expenses()

    def load_expenses(self) -> None:
        """Load expenses from a JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.expenses = json.load(f)
                    if self.expenses:  # Check if the file has data
                        self.next_id = (
                            max(expense["id"] for expense in self.expenses) + 1
                        )
            except json.JSONDecodeError:
                print(f"Error reading {self.filename}. The file may be corrupted.")
                self.expenses = []  # Reset expenses if the file is corrupted
                self.next_id = 1  # Reset next_id
        else:
            print(f"{self.filename} not found. Starting with an empty expense list.")
            self.expenses = []  # No file, so start with an empty list

    def save_expenses(self):
        """Save expenses to a JSON file."""
        with open(self.filename, "w") as f:
            json.dump(
                [
                    {**expense, "date": expense["date"].strftime("%Y-%m-%d")}
                    for expense in self.expenses
                ],
                f,
                indent=4,
            )

    def add_expense(self, description: str, amount: float) -> None:
        expense = {
            "id": self.next_id,
            "date": datetime.now().date(),
            "description": description,
            "amount": amount,
        }
        self.expenses.append(expense)
        print(f"Expense added successfully (ID: {expense['id']})")
        self.next_id += 1
        self.save_expenses()  # Save after adding an expense

    def delete_expense(self, id: int) -> None:
        self.expenses = [expense for expense in self.expenses if expense["id"] != id]
        self.save_expenses()  # Save after deleting an expense

    def expense_summary(self, month=None):
        total_expenses = []
        if month:
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
                if expense_date.month == month:
                    total_expenses.append(expense["amount"])

            month_name = datetime(datetime.now().year, month, 1).strftime("%B")
            print(f"Total expenses for {month_name}: ${sum(total_expenses)}")
        else:
            for expense in self.expenses:
                total_expenses.append(expense["amount"])
            print(f"Total expenses: ${sum(total_expenses)}")

    def list_expenses(self) -> PrettyTable:
        expenses_table = prettytable.PrettyTable()
        for expense in self.expenses:
            expenses_table.field_names = list(expense.keys())
            expenses_table.add_row(list(expense.values()))
        return expenses_table


# Initialize ExpenseTracker instance
tracker = ExpenseTracker()


@click.group()
def app():
    """Expense Tracker CLI."""
    pass


@app.command()
@click.option(
    "--description", prompt="Description", help="The description of the expense."
)
@click.option(
    "--amount", type=float, prompt="Amount", help="The amount for the expense."
)
def add(description: str, amount: float):
    """Add a new expense."""
    tracker.add_expense(description, amount)
    click.echo(f"Expense added successfully: (ID: {tracker.next_id}).")


@app.command()
@click.option("--id", type=int, prompt="ID", help="ID of the expenses to delete.")
def delete(id):
    """Delete an expense based on id"""
    tracker.delete_expense(id)
    click.echo("Expense delete successfully")


@app.command(name="list")
def list_expenses():
    """List all expenses"""
    table = tracker.list_expenses()
    click.echo(table)


@app.command()
@click.option("--month", type=int, default=None, help="Summary of expenses per month")
def summary(month):
    """Get a summary of expenses"""
    tracker.expense_summary(month)


if __name__ == "__main__":
    app()
