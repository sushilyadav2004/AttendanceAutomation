from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.api.employee import router as employees_router
from app.api.attendance import router as attendance_router
from app.api.reports import router as reports_router
from app.api.file_monitoring import router as file_monitoring_router
from app.api.settings import router as settings_router
from app.database.connection import SessionLocal
from app.services.dashboard_service import get_dashboard_data
from app.services.scheduler_service import start_scheduler
from app.core.logger import logger
from app.core.templates import templates
import threading
app = FastAPI(
    title="Attendance Automation System"
)
@app.on_event("startup")
def startup_event():

    try:
        logger.info(
            "Starting Attendance Scheduler..."
        )
        scheduler_thread = threading.Thread(
            target=start_scheduler,
            daemon=True
        )
        scheduler_thread.start()

        logger.info(
            "Attendance Scheduler thread started."
        )

    except Exception as ex:

        logger.exception(
            f"Failed to start Attendance Scheduler. {ex}"
        )

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# Employee Router
app.include_router(employees_router)

# Attendance Router
app.include_router(attendance_router)

# Reports Router
app.include_router(reports_router)

# File Monitoring Router
app.include_router(file_monitoring_router)

# Settings Router
app.include_router(settings_router)


@app.get("/")
def dashboard(request: Request):

    db = None
    try:

        db = SessionLocal()

        dashboard_data = get_dashboard_data(db)

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "request": request,
                "dashboard": dashboard_data
            }
        )

    except Exception as ex:

        logger.exception(
            f"Dashboard loading failed. {ex}"
        )

        raise

    finally:

        if db:
            db.close()
@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
if __name__ == "__main__":

    import uvicorn

    logger.info(
        "Attendance Automation web application started."
    )
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )