from app.services.file_monitor import get_excel_files
from app.core.logger import logger


input_folder = "files/input"


try:

    logger.info("File monitor test started.")

    files = get_excel_files(
        input_folder
    )

    print("\nExcel Files Found:")
    print("-----------------------------")

    if files:

        for file_path in files:
            print(file_path)

    else:

        print("No Excel files found.")

except Exception as e:

    logger.exception(
        "File monitor test failed."
    )

    print("File monitoring failed!")
    print(f"Error: {e}")

finally:

    logger.info(
        "File monitor test finished."
    )