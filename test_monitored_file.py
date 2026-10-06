from app.database.connection import SessionLocal
from app.database.repositories.monitored_file_repository import (
    add_monitored_file,
    mark_file_processed
)
from app.core.logger import logger


file_name = "attendance.xlsx"
file_path = "files/input/attendance.xlsx"

db = None

try:

    logger.info("Monitored file test started.")

    db = SessionLocal()

    # Add file to MonitoredFiles
    monitored_file = add_monitored_file(
        db,
        file_name,
        file_path
    )

    print("\nMonitored File:")
    print("-----------------------------")
    print("File Name:", monitored_file.FileName)
    print("File Path:", monitored_file.FilePath)
    print("Status:", monitored_file.Status)

    # Mark file as processed
    processed_file = mark_file_processed(
        db,
        file_name
    )

    print("\nAfter Processing:")
    print("-----------------------------")
    print("File Name:", processed_file.FileName)
    print("Status:", processed_file.Status)
    print("Processed At:", processed_file.ProcessedAt)

except Exception as e:

    logger.exception(
        "Monitored file test failed."
    )

    print("Monitored file test failed!")
    print(f"Error: {e}")

finally:

    if db:
        db.close()
        logger.info("Database session closed.")

    logger.info("Monitored file test finished.")