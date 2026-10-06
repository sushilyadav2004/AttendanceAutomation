from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

from app.database.connection import SessionLocal
from app.models.schedule import ScheduleSetting

from app.core.templates import templates
from app.core.logger import logger


router = APIRouter()


@router.get("/settings")
def settings_page(request: Request):

    db = None

    try:

        db = SessionLocal()

        settings = (
            db.query(ScheduleSetting)
            .order_by(
                ScheduleSetting.Id
            )
            .all()
        )

        logger.info(
            f"Schedule settings page loaded. "
            f"Count: {len(settings)}"
        )

        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context={
                "request": request,
                "settings": settings
            }
        )

    except Exception as ex:

        logger.exception(
            f"Failed to load schedule settings page. {ex}"
        )

        raise

    finally:

        if db:
            db.close()


@router.get("/settings/edit/{setting_id}")
def edit_settings_page(
    request: Request,
    setting_id: int
):

    db = None

    try:

        db = SessionLocal()

        setting = (
            db.query(ScheduleSetting)
            .filter(
                ScheduleSetting.Id == setting_id
            )
            .first()
        )

        if not setting:

            logger.warning(
                f"Schedule setting not found: {setting_id}"
            )

            return RedirectResponse(
                url="/settings",
                status_code=303
            )

        return templates.TemplateResponse(
            request=request,
            name="edit_settings.html",
            context={
                "request": request,
                "setting": setting
            }
        )

    except Exception as ex:

        logger.exception(
            f"Failed to load schedule edit page. {ex}"
        )

        raise

    finally:

        if db:
            db.close()


@router.post("/settings/edit/{setting_id}")
def update_settings(
    setting_id: int,
    interval_minutes: int = Form(...),
    is_active: bool = Form(False)
):

    db = None

    try:

        db = SessionLocal()

        setting = (
            db.query(ScheduleSetting)
            .filter(
                ScheduleSetting.Id == setting_id
            )
            .first()
        )

        if not setting:

            logger.warning(
                f"Schedule setting not found: {setting_id}"
            )

            return RedirectResponse(
                url="/settings",
                status_code=303
            )

        if interval_minutes <= 0:

            raise ValueError(
                "Interval must be greater than 0."
            )

        setting.IntervalMinutes = interval_minutes
        setting.IsActive = is_active

        db.commit()
        db.refresh(setting)

        logger.info(
            f"Schedule updated successfully. "
            f"ID: {setting_id}, "
            f"Interval: {interval_minutes}, "
            f"Active: {is_active}"
        )

        return RedirectResponse(
            url="/settings",
            status_code=303
        )

    except Exception as ex:

        if db:
            db.rollback()

        logger.exception(
            f"Failed to update schedule settings. {ex}"
        )

        raise

    finally:

        if db:
            db.close()