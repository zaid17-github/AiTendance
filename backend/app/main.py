from app.attendance import save_attendance
from app.face_utils import encode_face, detect_faces

import cv2
import os
import shutil

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"


# Home Route
@app.get("/")
def home():

    return {
        "project": "AiTendance",
        "status": "Backend Running Successfully"
    }


# Register Student
@app.post("/register")
async def register_student(
    name: str = Form(...),
    image: UploadFile = File(...)
):

    # Create uploads folder if not exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"{name}.jpg"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        "message": f"{name} registered successfully"
    }


# Classroom Scanner
@app.get("/scan")
def scan_faces():

    known_face_encodings = []
    known_face_names = []

    # Fast preload registered students
    student_files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".jpg")
    ]

    for file in student_files:

        path = os.path.join(
            UPLOAD_FOLDER,
            file
        )

        image = cv2.imread(path)

        if image is None:
            continue

        encoding = encode_face(path)

        if encoding is not None:

            known_face_encodings.append(
                encoding
            )

            known_face_names.append(
                file.split(".")[0]
            )

    # Faster webcam startup on Windows
    video_capture = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    # Webcam optimization
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_capture.set(cv2.CAP_PROP_FPS, 15)

    detected_students = set()

    # Stable recognition counter
    frame_detection_count = {}

    print("AiTendance Classroom Scanner Started...")

    # Alternate frame processing
    process_this_frame = True

    face_locations = []
    names = []

    while True:

        ret, frame = video_capture.read()

        if not ret:
            break

        # Resize for performance
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.35,
            fy=0.35
        )

        # Process alternate frames
        if process_this_frame:

            face_locations, names = detect_faces(
                small_frame,
                known_face_encodings,
                known_face_names
            )

        process_this_frame = not process_this_frame

        # Scale locations back
        scaled_locations = []

        for (top, right, bottom, left) in face_locations:

            scaled_locations.append(
                (
                    int(top / 0.35),
                    int(right / 0.35),
                    int(bottom / 0.35),
                    int(left / 0.35)
                )
            )

        # Draw detections
        for ((top, right, bottom, left), name) in zip(
            scaled_locations,
            names
        ):

            # Stable recognition logic
            if name not in frame_detection_count:
                frame_detection_count[name] = 0

            frame_detection_count[name] += 1

            # Mark present only after stable detection
            if frame_detection_count[name] >= 5:
                detected_students.add(name)

            # Face rectangle
            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            # Name label
            cv2.putText(
                frame,
                f"{name} - Present",
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # Present count
        cv2.putText(
            frame,
            f"Present Count: {len(detected_students)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow(
            "AiTendance Classroom Scanner",
            frame
        )

        # Press Q to stop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()

    cv2.destroyAllWindows()

    # Save attendance report
    attendance_file = save_attendance(
        list(detected_students)
    )

    return {
        "present_students": list(detected_students),
        "attendance_file": attendance_file
    }


# Download Latest Attendance Excel
@app.get("/download-attendance")
def download_attendance():

    reports_folder = os.path.abspath("reports")

    # Get only Excel files
    files = [
        f for f in os.listdir(reports_folder)
        if f.endswith(".xlsx")
    ]

    if len(files) == 0:

        return {
            "message": "No attendance reports found"
        }

    # Latest file
    latest_file = max(
        files,
        key=lambda f: os.path.getctime(
            os.path.join(reports_folder, f)
        )
    )

    file_path = os.path.join(
        reports_folder,
        latest_file
    )

    return FileResponse(
        path=file_path,
        filename=latest_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )