from app.database.connection import SessionLocal
from app.services.report_generator import generate_attendance_report
from app.core.logger import logger


output_file = "files/reports/Attendance_Report.xlsx"

db = None

try:

    logger.info("Report test started.")

    db = SessionLocal()

    report = generate_attendance_report(
        db,
        output_file
    )

    print("\nReport generated successfully!")
    print("--------------------------------")
    print("Report:", report)

except Exception as e:

    logger.exception(
        "Report test failed."
    )

    print("Report generation failed!")
    print(f"Error: {e}")

finally:

    if db:
        db.close()
        logger.info("Database session closed.")

    logger.info("Report test finished.")