from fastapi import APIRouter, Request

from app.database.connection import SessionLocal
from app.models.employee import Employee
from app.core.templates import templates
from app.core.logger import logger

router = APIRouter()


@router.get("/employees")
def employees_page(request: Request):

    db = None

    try:
        db = SessionLocal()

        employees = (
            db.query(Employee)
            .filter(Employee.IsActive == True)
            .order_by(Employee.EmployeeId)
            .all()
        )

        logger.info(
            f"Employees page loaded. Count: {len(employees)}"
        )

        return templates.TemplateResponse(
            request=request,
            name="employee.html",
            context={
                "request": request,
                "employees": employees
            }
        )

    except Exception as ex:
        logger.exception(
            f"Failed to load employees page. {ex}"
        )
        raise

    finally:
        if db:
            db.close()