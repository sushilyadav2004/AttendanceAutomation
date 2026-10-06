from app.services.scheduler_service import get_schedule_settings


try:

    interval = get_schedule_settings()

    print("\nSchedule Configuration:")
    print("-----------------------------")

    if interval:
        print("Interval:", interval, "minutes")
    else:
        print("No active schedule found.")

except Exception as e:

    print("Schedule configuration failed!")
    print(f"Error: {e}")