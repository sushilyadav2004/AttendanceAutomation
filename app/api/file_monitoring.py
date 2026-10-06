from fastapi import APIRouter, Request

from app.database.connection import SessionLocal
from app.models.monitored_file import MonitoredFile

from app.core.templates import templates
from app.core.logger import logger


router = APIRouter()


@router.get("/file-monitoring")
def file_monitoring_page(request: Request):

    db = None

    try:

        db = SessionLocal()

        monitored_files = (
            db.query(MonitoredFile)
            .order_by(
                MonitoredFile.CreatedAt.desc()
            )
            .all()
        )

        logger.info(
            f"File monitoring page loaded. "
            f"Count: {len(monitored_files)}"
        )

        return templates.TemplateResponse(
            request=request,
            name="file_monitoring.html",
            context={
                "request": request,
                "monitored_files": monitored_files
            }
        )

    except Exception as ex:

        logger.exception(
            f"Failed to load file monitoring page. {ex}"
        )

        raise

    finally:

        if db:
            db.close()