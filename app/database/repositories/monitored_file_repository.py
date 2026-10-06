from datetime import datetime
from app.models.monitored_file import MonitoredFile
from app.core.logger import logger
def get_existing_file(db, file_name):
    """
    Check whether the file already exists in MonitoredFiles.
    """
    try:
        return (
            db.query(MonitoredFile)
            .filter(
                MonitoredFile.FileName == file_name
            )
            .first()
        )
    except Exception:
        logger.exception(
            f"Failed to check monitored file: {file_name}"
        )
        raise
def add_monitored_file(
    db,
    file_name,
    file_path,
    file_date=None
):
    """
    Add a new file to MonitoredFiles.
    """
    try:
        existing_file = get_existing_file(
            db,
            file_name
        )
        if existing_file:
            logger.info(
                f"File already exists: {file_name}"
            )
            return existing_file
        monitored_file = MonitoredFile(
            FileName=file_name,
            FilePath=file_path,
            FileDate=file_date,
            Status="Pending"
        )
        db.add(monitored_file)
        db.commit()
        db.refresh(monitored_file)
        logger.info(
            f"File added to monitoring: {file_name}"
        )
        return monitored_file
    except Exception:
        db.rollback()
        logger.exception(
            f"Failed to add monitored file: {file_name}"
        )
        raise
def mark_file_processed(db, file_name):
    """
    Mark file as successfully processed.
    """
    try:
        monitored_file = get_existing_file(
            db,
            file_name
        )
        if not monitored_file:
            logger.warning(
                f"File not found in MonitoredFiles: {file_name}"
            )
            return None
        monitored_file.Status = "Processed"
        monitored_file.ProcessedAt = datetime.now()
        db.commit()
        db.refresh(monitored_file)
        logger.info(
            f"File marked as processed: {file_name}"
        )
        return monitored_file
    except Exception:
        db.rollback()
        logger.exception(
            f"Failed to mark file as processed: {file_name}"
        )
        raise