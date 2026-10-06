import pandas as pd
REQUIRED_COLUMNS = [
    "EmployeeId",
    "LoginTime",
    "LogoutTime"
]
def read_attendance_file(file_path: str) -> pd.DataFrame:
    """
    Read attendance Excel file and validate required columns.
    """
    df = pd.read_excel(file_path)
    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()
    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Missing columns: {', '.join(missing_columns)}"
        )
    # Keep only required columns
    df = df[REQUIRED_COLUMNS]
    # Remove completely empty rows
    df = df.dropna(how="all")
    return df