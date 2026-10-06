from apscheduler.schedulers.blocking import BlockingScheduler

from app.database.connection import SessionLocal
from app.models.schedule import ScheduleSetting

from app.services.file_monitor import get_excel_files
from app.services.attendance_processor import process_attendance_file

from app.core.logger import logger


INPUT_FOLDER = "files/input"


def get_schedule_settings():

    db = None

    try:

        db = SessionLocal()

        setting = (
            db.query(ScheduleSetting)
            .filter(
                ScheduleSetting.ScheduleName
                == "Attendance File Check",
                ScheduleSetting.IsActive == True
            )
            .first()
        )

        if not setting:

            logger.warning(
                "Active attendance schedule not found."
            )

            return None

        logger.info(
            f"Schedule loaded: "
            f"{setting.IntervalMinutes} minutes"
        )

        return setting.IntervalMinutes

    except Exception as ex:

        logger.exception(
            f"Failed to load schedule settings. {ex}"
        )

        raise

    finally:

        if db:
            db.close()


def check_attendance_files():

    try:

        logger.info(
            "Scheduled attendance check started."
        )

        files = get_excel_files(
            INPUT_FOLDER
        )

        if not files:

            logger.info(
                "No Excel files found."
            )

            return

        for file_path in files:

            try:

                result = process_attendance_file(
                    file_path
                )

                logger.info(
                    f"File processing result: {result}"
                )

            except Exception as ex:

                logger.exception(
                    f"Failed to process file: {file_path}. {ex}"
                )

    except Exception as ex:

        logger.exception(
            f"Scheduled attendance check failed. {ex}"
        )

    finally:

        logger.info(
            "Scheduled attendance check finished."
        )


def start_scheduler():

    try:

        interval_minutes = get_schedule_settings()

        if not interval_minutes:

            logger.warning(
                "Scheduler was not started."
            )

            print(
                "Scheduler configuration not found."
            )

            return

        scheduler = BlockingScheduler()

        scheduler.add_job(
            check_attendance_files,
            "interval",
            minutes=interval_minutes,
            id="attendance_file_check",
            replace_existing=True
        )

        logger.info(
            f"Scheduler started. "
            f"Interval: {interval_minutes} minutes."
        )

        print(
            f"Scheduler started. "
            f"Checking every {interval_minutes} minutes."
        )

        scheduler.start()

    except KeyboardInterrupt:

        logger.info(
            "Scheduler stopped by user."
        )

        print("Scheduler stopped.")

    except Exception as ex:

        logger.exception(
            f"Scheduler failed. {ex}"
        )

        raise