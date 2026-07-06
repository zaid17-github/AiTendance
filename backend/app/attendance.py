import pandas as pd
from datetime import datetime
import os

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"


def save_attendance(present_students):

    all_students = []

    # Get all registered students
    for file in os.listdir(UPLOAD_FOLDER):

        if file.endswith(".jpg"):
            student_name = file.split(".")[0]
            all_students.append(student_name)

    attendance_data = []

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for student in all_students:

        status = "Present"

        if student not in present_students:
            status = "Absent"

        attendance_data.append({
            "Name": student,
            "Status": status,
            "Time": current_time if status == "Present" else "-"
        })

    df = pd.DataFrame(attendance_data)

    file_name = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    file_path = os.path.join(REPORT_FOLDER, file_name)

    df.to_excel(file_path, index=False)

    return file_path