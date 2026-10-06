import os
import glob

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from app.core.templates import templates
from app.core.logger import logger


router = APIRouter()

REPORT_FOLDER = "files/reports"


def get_latest_report():

    try:

        report_pattern = os.path.join(
            REPORT_FOLDER,
            "Attendance_Report_*.xlsx"
        )

        report_files = glob.glob(
            report_pattern
        )

        if not report_files:
            logger.info(
                "No attendance reports found."
            )
            return None

        latest_report = max(
            report_files,
            key=os.path.getmtime
        )

        logger.info(
            f"Latest report found: {latest_report}"
        )

        return latest_report

    except Exception as ex:

        logger.exception(
            f"Failed to find latest attendance report. {ex}"
        )

        raise


@router.get("/reports")
def reports_page(request: Request):

    try:

        latest_report = get_latest_report()

        if latest_report:

            report_file = os.path.basename(
                latest_report
            )

            report_exists = True

        else:

            report_file = None
            report_exists = False

        logger.info(
            f"Reports page loaded. "
            f"Latest report: {report_file}"
        )

        return templates.TemplateResponse(
            request=request,
            name="reports.html",
            context={
                "request": request,
                "report_exists": report_exists,
                "report_file": report_file
            }
        )

    except Exception as ex:

        logger.exception(
            f"Failed to load reports page. {ex}"
        )

        raise


@router.get("/reports/download")
def download_report():

    try:

        latest_report = get_latest_report()

        if not latest_report:

            logger.warning(
                "Attendance report not found."
            )

            return {
                "message": "Attendance report not found."
            }

        logger.info(
            f"Downloading report: {latest_report}"
        )

        return FileResponse(
            path=latest_report,
            filename=os.path.basename(
                latest_report
            ),
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

    except Exception as ex:

        logger.exception(
            f"Failed to download attendance report. {ex}"
        )

        raise