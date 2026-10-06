import os

from app.core.logger import logger


def get_excel_files(input_folder):
    """
    Find all Excel files from the input folder.
    """

    try:

        logger.info(
            f"Checking input folder: {input_folder}"
        )

        if not os.path.exists(input_folder):

            logger.warning(
                f"Input folder does not exist: {input_folder}"
            )

            return []

        excel_files = []

        for file_name in os.listdir(input_folder):

            if file_name.lower().endswith(
                (".xlsx", ".xls")
            ):

                file_path = os.path.join(
                    input_folder,
                    file_name
                )

                if os.path.isfile(file_path):

                    excel_files.append(file_path)

        logger.info(
            f"Found {len(excel_files)} Excel file(s)."
        )

        return excel_files

    except Exception as ex:

        logger.exception(
            f"Failed to scan input folder. {ex}"
        )

        raise