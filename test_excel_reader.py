from app.services.excel_reader import read_attendance_file


file_path = "files/input/attendance.xlsx"

try:
    data = read_attendance_file(file_path)

    print("Excel file read successfully!")
    print()
    print(data)

except Exception as e:
    print("Excel file processing failed!")
    print(e)