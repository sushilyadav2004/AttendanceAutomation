from app.services.scheduler_service import (
    check_attendance_files
)


try:

    print("Running attendance file check...")

    check_attendance_files()

    print("Attendance file check completed.")

except Exception as e:

    print("Scheduler test failed!")
    print(f"Error: {e}")
