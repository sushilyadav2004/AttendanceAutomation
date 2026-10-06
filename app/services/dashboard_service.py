from datetime import date

from sqlalchemy import func

from app.core.logger import logger
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.monitored_file import MonitoredFile


def get_dashboard_data(db):

    try:

        logger.info("Fetching dashboard data.")

        # Total active employees
        total_employees = (
            db.query(func.count(Employee.Id))
            .filter(Employee.IsActive == True)
            .scalar()
        )

        # Today's date
        today = date.today()

        # Present employees today
        present_today = (
            db.query(func.count(Attendance.Id))
            .filter(
                Attendance.AttendanceDate == today,
                Attendance.Status == "Present"
            )
            .scalar()
        )

        # Absent employees today
        absent_today = (
            db.query(func.count(Attendance.Id))
            .filter(
                Attendance.AttendanceDate == today,
                Attendance.Status == "Absent"
            )
            .scalar()
        )

        # Processed files
        files_processed = (
            db.query(func.count(MonitoredFile.Id))
            .filter(
                MonitoredFile.Status == "Processed"
            )
            .scalar()
        )

        dashboard_data = {
            "total_employees": total_employees or 0,
            "present_today": present_today or 0,
            "absent_today": absent_today or 0,
            "files_processed": files_processed or 0
        }

        logger.info(
            f"Dashboard data loaded: {dashboard_data}"
        )

        return dashboard_data

    except Exception as ex:

        logger.exception(
            f"Failed to load dashboard data. {ex}"
        )

        raise