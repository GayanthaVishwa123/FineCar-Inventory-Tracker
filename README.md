FineCar Inventory Tracker

FineCar Inventory Tracker is an automated system designed for managing vehicle inventory. This project is developed using Python and PostgreSQL, featuring an automated testing process through GitHub Actions.
🚀 Features

    Inventory Management: Efficient tracking and management of vehicle stock data.

    CI/CD Pipeline: Automated testing triggered on every push to the repository.

    Database Service: Integration with a PostgreSQL 15 service for reliable database testing.

    Security: Database credentials are securely managed using GitHub Secrets.

🛠 Tech Stack

    Backend: Python (FastAPI/Python Script)

    Database: PostgreSQL

    Testing: Pytest

    CI/CD: GitHub Actions (Composite Actions)

⚙️ CI/CD Pipeline Workflow

The project's CI/CD pipeline consists of the following stages:

    Checkout: Clones the code to the runner.

    Environment Setup: Installs Python and all required dependencies.

    Database Service: Provisions a temporary Postgres service for testing.

    Testing: Executes pytest to verify database connectivity and logic.

🔐 Security Setup

To maintain security, database credentials (User, Password, DB Name) are not hardcoded. They are managed via GitHub Repository Secrets.

To run this pipeline successfully in your own fork, ensure the following secrets are configured in your Repository Settings:

    DB_USER

    DB_PASSWORD

    DB_NAME

📦 Installation and Testing

    Clone the repository:
    Bash

    git clone https://github.com/GayanthaVishwa123/FineCar-Inventory-Tracker.git

    Install the required dependencies:
    Bash

    pip install -r requirements.txt

    Run the tests:
    Bash

    pytest
