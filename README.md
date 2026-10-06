# Attendance Automation System

A FastAPI web application for monitoring employee attendance, processing Excel
attendance files, and generating downloadable reports backed by Microsoft SQL
Server.

## Features

- Dashboard showing employee and daily attendance totals.
- Employee, attendance, processed-file, and schedule views.
- Reads `.xlsx` and `.xls` files containing `EmployeeId`, `LoginTime`, and
  `LogoutTime` columns.
- Compares submitted attendance with active employees in SQL Server and records
  employees missing from a file as absent.
- Periodically checks the input folder using the active
  `Attendance File Check` schedule.
- Generates formatted Excel attendance reports.
- Health endpoint at `/health`.

## Requirements

- Windows
- Python 3.10 or later
- Microsoft SQL Server and the Microsoft ODBC Driver for SQL Server
- A SQL Server database with the tables expected by the application

The database schema must be provisioned before running the app. The SQLAlchemy
models are in `app/models/`; this project does not currently include a database
migration or schema-creation script.

## Setup

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root with the SQL Server connection
settings:

```dotenv
DB_SERVER=localhost
DB_NAME=AttendanceDB
DB_DRIVER=ODBC Driver 18 for SQL Server
```

The application uses Windows integrated authentication
(`Trusted_Connection=yes`); configure SQL Server access for the Windows account
that runs the app. Update the example values for your SQL Server and database.
Do not commit `.env` or put database credentials in source control.

## Run

From the project root, start the development server:

```powershell
python -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Check the health endpoint at
<http://127.0.0.1:8000/health>.

Create the input folder if it does not exist, then place attendance workbooks
in `files/input/`. The scheduler scans this folder at the interval configured
in the database. Generated reports are saved in `files/reports/`, and
application logs are written to `logs/app.log`.

## Attendance workbook format

Each workbook must include these column headers (additional columns are
ignored):

| Column | Description |
| --- | --- |
| `EmployeeId` | Employee identifier matching an active SQL Server employee |
| `LoginTime` | Employee login time |
| `LogoutTime` | Employee logout time |

Column headers may have surrounding spaces; completely empty rows are ignored.

## Tests

Install `pytest` in the active virtual environment if it is not already
available, then run the test suite from the project root:

```powershell
python -m pytest
```
