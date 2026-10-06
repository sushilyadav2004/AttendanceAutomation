from fastapi import APIRouter, Request

from app.database.connection import SessionLocal
from app.models.attendance import Attendance
from app.models.employee import Employee

from app.core.templates import templates
from app.core.logger import logger


router = APIRouter()


@router.get("/attendance")
def attendance_page(request: Request):

    db = None

    try:

        db = SessionLocal()

        attendance_records = (
            db.query(
                Attendance,
                Employee.EmployeeName,
                Employee.Department
            )
            .join(
                Employee,
                Attendance.EmployeeId == Employee.EmployeeId
            )
            .order_by(
                Attendance.AttendanceDate.desc(),
                Attendance.EmployeeId
            )
            .all()
        )

        logger.info(
            f"Attendance page loaded. Count: {len(attendance_records)}"
        )

        return templates.TemplateResponse(
            request=request,
            name="attendance.html",
            context={
                "request": request,
                "attendance_records": attendance_records
            }
        )

    except Exception as ex:

        logger.exception(
            f"Failed to load attendance page. {ex}"
        )

        raise

    finally:

        if db:
            db.close()