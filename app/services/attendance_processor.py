import os

from app.core.logger import logger
from app.database.connection import SessionLocal

from app.database.repositories.monitored_file_repository import (
    add_monitored_file,
    mark_file_processed
)

from app.database.repositories.attendance_repository import (
    save_attendance
)

from app.services.excel_reader import (
    read_attendance_file
)

from app.services.attendance_comparator import (
    compare_attendance
)

from app.services.report_generator import (
    generate_attendance_report
)


def process_attendance_file(file_path):

    db = None

    try:

        logger.info(
            f"Attendance processing started: {file_path}"
        )

        # Get file information
        file_name = os.path.basename(file_path)

        # Create database session
        db = SessionLocal()

        logger.info("Database session created.")

        # Check/add file in MonitoredFiles
        monitored_file = add_monitored_file(
            db,
            file_name,
            file_path
        )

        # If file is already processed, skip it
        if monitored_file.Status == "Processed":

            logger.info(
                f"File already processed. Skipping: {file_name}"
            )

            return {
                "status": "Skipped",
                "file": file_name
            }

        # Read Excel file
        attendance_data = read_attendance_file(
            file_path
        )

        logger.info(
            f"Excel file read successfully: {file_name}"
        )

        # Compare with SQL Employees
        attendance_records = compare_attendance(
            db,
            attendance_data
        )

        logger.info(
            "Attendance comparison completed."
        )

        # Save attendance
        save_result = save_attendance(
            db,
            attendance_records,
            file_name
        )

        logger.info(
            f"Attendance saved. "
            f"Inserted: {save_result['inserted']}, "
            f"Updated: {save_result['updated']}"
        )

# Generate report
        report_path = generate_attendance_report(
         db
)

        logger.info(
    f"Report generated: {report_path}"
)

        # Mark file as processed
        mark_file_processed(
         db,
            file_name
        )

        logger.info(
            f"File marked as processed: {file_name}"
        )

        return {
            "status": "Processed",
            "file": file_name,
            "report": report_path,
            "inserted": save_result["inserted"],
            "updated": save_result["updated"]
        }

    except Exception as ex:

        if db:
            db.rollback()

        logger.exception(
            f"Attendance processing failed: {file_path} - {ex}"
        )

        raise

    finally:

        if db:
            db.close()

            logger.info(
                "Database session closed."
            )

        logger.info(
            f"Attendance processing finished: {file_path}"
        )