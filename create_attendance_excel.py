import os
from openpyxl import Workbook

# Attendance folder
attendance_folder = "attendance"

# Create folder if it doesn't exist
os.makedirs(attendance_folder, exist_ok=True)

# Excel file path
excel_file = os.path.join(attendance_folder, "attendance.xlsx")

# Create Excel file if it doesn't exist
if not os.path.exists(excel_file):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Attendance"

    # Header row
    sheet.append([
        "Date",
        "Time",
        "Name",
        "Roll",
        "Department",
        "Status"
    ])

    workbook.save(excel_file)

    print("Attendance Excel file created successfully!")
    print("File:", excel_file)

else:
    print("Attendance Excel file already exists!")
    print("File:", excel_file)