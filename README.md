# Expense Tracker CLI

A simple command-line interface (CLI) application to manage your finances. This project is inspired by the Expense Tracker project outlined on [roadmap.sh](https://roadmap.sh/projects/expense-tracker).

## Features

* **Add Expenses:**  Record new expenses with a description and amount.
* **List Expenses:** View all recorded expenses in a tabular format.
* **Delete Expenses:** Remove expenses by their unique ID.
* **Expense Summary:** Get a summary of total expenses, optionally filtered by month.
* **Data Persistence:** Expenses are saved to `expenses.json` so your data is preserved between sessions.

## Installation

1.  Clone the repository:

    ```bash
    git clone [invalid URL removed]  # Replace with your repo URL
    cd expense-tracker
    ```

2.  Install the required dependencies using Poetry:

    ```bash
    poetry install
    ```

    If you don't have Poetry installed, follow the instructions on their website: [https://python-poetry.org/](https://python-poetry.org/)

## Usage

The Expense Tracker CLI provides the following commands:

*   **`add`:** Add a new expense.

    ```bash
    poetry run expense-tracker add --description "Groceries" --amount 50.00
    ```

*   **`list`:** List all expenses.

    ```bash
    poetry run expense-tracker list
    ```

*   **`delete`:** Delete an expense by ID.

    ```bash
    poetry run expense-tracker delete --id 3  # Replace 3 with the actual ID
    ```

*   **`summary`:** Get a summary of expenses.  You can also provide a month number (1-12) to see a monthly summary.

    ```bash
    poetry run expense-tracker summary
    poetry run expense-tracker summary --month 3  # Summary for March
    ```

## Project Structure

expense-tracker
├── LICENSE         # Optional license file
├── README.md       # This file
├── data.json       # Example data file (might be empty initially)
├── expense-tracker.py  # The main Python script
├── expenses.json    # Stores expense data in JSON format
├── poetry.lock     # Poetry's lock file for dependency management
└── pyproject.toml  # Poetry's project configuration file


## Data Storage

Expenses are stored in a JSON file named `expenses.json` in the project's root directory.  The format of each expense entry is:

```json
{
  "id": 1,
  "date": "2024-10-27",
  "description": "Coffee",
  "amount": 5.00
}
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License
[LICENSE](./LICENSE)
