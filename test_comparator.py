from app.database.connection import SessionLocal
from app.services.excel_reader import read_attendance_file
from app.services.attendance_comparator import compare_attendance
from app.database.repositories.attendance_repository import save_attendance
from app.core.logger import logger


file_path = "files/input/attendance.xlsx"

db = None

try:

    logger.info("Attendance process started.")

    db = SessionLocal()

    logger.info("Database session created.")

    # Read Excel
    attendance_data = read_attendance_file(file_path)

    logger.info("Excel file read successfully.")

    # Compare Excel with Employees table
    result = compare_attendance(
        db,
        attendance_data
    )

    logger.info("Attendance comparison completed.")

    # Save attendance to SQL Server
    save_attendance(
        db,
        result,
        "attendance.xlsx"
    )

    logger.info("Attendance saved successfully.")

    print("\nAttendance records saved successfully!")

except Exception as e:

    logger.exception(
        "Attendance process failed."
    )

    print("Attendance process failed!")
    print(f"Error: {e}")

finally:

    if db:
        db.close()
        logger.info("Database session closed.")

    logger.info("Attendance process finished.")