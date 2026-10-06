from datetime import date
import pandas as pd
from sqlalchemy.orm import Session
from app.models.employee import Employee
def compare_attendance(
    db: Session,
    attendance_data: pd.DataFrame
):
    """
    Compare Excel attendance data with active employees
    from SQL Server.
    """

    # Get all active employees from SQL
    employees = (
        db.query(Employee)
        .filter(Employee.IsActive == True)
        .all()
    )
    result = []
    # Create quick lookup from Excel
    attendance_lookup = {
        str(row["EmployeeId"]).strip(): row
        for _, row in attendance_data.iterrows()
    }
    # Compare every SQL employee with Excel
    for employee in employees:

        employee_id = employee.EmployeeId

        if employee_id in attendance_lookup:

            row = attendance_lookup[employee_id]

            result.append({
                "EmployeeId": employee_id,
                "EmployeeName": employee.EmployeeName,
                "Department": employee.Department,
                "AttendanceDate": date.today(),
                "Status": "Present",
                "LoginTime": row["LoginTime"],
                "LogoutTime": row["LogoutTime"]
            })

        else:

            result.append({
                "EmployeeId": employee_id,
                "EmployeeName": employee.EmployeeName,
                "Department": employee.Department,
                "AttendanceDate": date.today(),
                "Status": "Absent",
                "LoginTime": None,
                "LogoutTime": None
            })
    return result