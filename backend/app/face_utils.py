import face_recognition
import cv2
import numpy as np


def encode_face(image_path):

    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0]


def detect_faces(frame, known_face_encodings, known_face_names):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # FAST classroom detection
    face_locations = face_recognition.face_locations(
        rgb_frame,
        model="hog"
    )

    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )

    detected_students = []

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(
            known_face_encodings,
            face_encoding,
            tolerance=0.48
        )

        face_distances = face_recognition.face_distance(
            known_face_encodings,
            face_encoding
        )

        if len(face_distances) == 0:
            continue

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:

            detected_name = known_face_names[
                best_match_index
            ]

            if detected_name not in detected_students:
                detected_students.append(detected_name)

    return face_locations, detected_students