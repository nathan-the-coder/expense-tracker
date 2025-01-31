import click
import json
import csv
from datetime import datetime
import os


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.next_id = 1
        self.load_expenses()

    def load_expenses(self):
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

    def add_expense(self, description, amount):
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

    def delete_expense(self, id):
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

    def export_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def export_to_csv(self, filename):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["description", "amount"])
            writer.writeheader()
            writer.writerows(self.expenses)


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
def add(description, amount):
    """Add a new expense."""
    tracker.add_expense(description, amount)
    click.echo(f"Added expense: {description} for {amount}.")


@app.command()
@click.option("--month", type=int, default=None, help="Summary of expenses per month")
def summary(month):
    """Get a summary of expenses"""
    tracker.expense_summary(month)


@app.command()
@click.argument("filename")
def export_json(filename):
    """Export expenses to a JSON file."""
    tracker.export_to_json(filename)
    click.echo(f"Exported expenses to {filename}.")


@app.command()
@click.argument("filename")
def export_csv(filename):
    """Export expenses to a CSV file."""
    tracker.export_to_csv(filename)
    click.echo(f"Exported expenses to {filename}.")


if __name__ == "__main__":
    app()

