from app.services.attendance_processor import (
    process_attendance_file
)
from app.core.logger import logger


file_path = "files/input/attendance.xlsx"


try:

    logger.info("Processor test started.")

    result = process_attendance_file(
        file_path
    )

    print("\nAttendance Processing Result:")
    print("--------------------------------")

    print("Status:", result["status"])
    print("File:", result["file"])

    if result["status"] == "Processed":

        print("Inserted:", result["inserted"])
        print("Updated:", result["updated"])
        print("Report:", result["report"])

except Exception as e:

    logger.exception(
        "Processor test failed."
    )

    print("Processing failed!")
    print(f"Error: {e}")

finally:

    logger.info(
        "Processor test finished."
    )