from app.models.attendance import Attendance
from app.core.logger import logger


def save_attendance(db, attendance_records, source_file):

    try:
        logger.info("Saving attendance records to database.")

        inserted_count = 0
        updated_count = 0

        for record in attendance_records:

            # Check whether attendance already exists
            existing_record = (
                db.query(Attendance)
                .filter(
                    Attendance.EmployeeId == record["EmployeeId"],
                    Attendance.AttendanceDate == record["AttendanceDate"]
                )
                .first()
            )

            if existing_record:

                # Update existing record
                existing_record.Status = record["Status"]
                existing_record.LoginTime = record["LoginTime"]
                existing_record.LogoutTime = record["LogoutTime"]
                existing_record.SourceFile = source_file

                updated_count += 1

                logger.info(
                    f"Attendance updated: {record['EmployeeId']}"
                )

            else:

                # Insert new record
                attendance = Attendance(
                    EmployeeId=record["EmployeeId"],
                    AttendanceDate=record["AttendanceDate"],
                    Status=record["Status"],
                    LoginTime=record["LoginTime"],
                    LogoutTime=record["LogoutTime"],
                    SourceFile=source_file
                )

                db.add(attendance)

                inserted_count += 1

                logger.info(
                    f"Attendance inserted: {record['EmployeeId']}"
                )

        db.commit()

        logger.info(
            f"Attendance processing completed. "
            f"Inserted: {inserted_count}, "
            f"Updated: {updated_count}"
        )

        return {
            "inserted": inserted_count,
            "updated": updated_count
        }

    except Exception as e:

        db.rollback()

        logger.exception(
            "Failed to save attendance records."
        )

        raise