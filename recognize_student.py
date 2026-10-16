import cv2
import json
import os
import numpy as np
from deepface import DeepFace

from attendance_manager import mark_attendance


# ==============================
# Load registered students
# ==============================

students_folder = "students"
students = []

print("Loading registered students...")

for filename in os.listdir(students_folder):

    if filename.endswith(".json"):

        file_path = os.path.join(students_folder, filename)

        with open(file_path, "r") as file:
            student = json.load(file)

        students.append(student)

        print(
            f"Loaded: {student['name']} | "
            f"Roll: {student['roll']}"
        )

print(f"\nTotal registered students: {len(students)}")


# ==============================
# Cosine similarity function
# ==============================

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


# ==============================
# Start camera
# ==============================

camera = cv2.VideoCapture(0)

print("\nCamera started.")
print("Press Q to quit.")


attendance_message = ""
message_time = 0


while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read camera.")
        break

    display_frame = frame.copy()

    try:

        # Detect faces
        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            enforce_detection=False
        )

        for face in faces:

            # Skip if no face detected
            if face["confidence"] < 0.50:
                continue

            facial_area = face["facial_area"]

            x = facial_area["x"]
            y = facial_area["y"]
            w = facial_area["w"]
            h = facial_area["h"]

            # Make sure coordinates are valid
            x = max(0, x)
            y = max(0, y)

            face_crop = frame[
                y:y+h,
                x:x+w
            ]

            if face_crop.size == 0:
                continue

            # ==============================
            # Generate face embedding
            # ==============================

            embedding_result = DeepFace.represent(
                img_path=face_crop,
                model_name="Facenet512",
                detector_backend="skip",
                enforce_detection=False
            )

            current_embedding = embedding_result[0]["embedding"]

            best_match = None
            best_similarity = -1

            # ==============================
            # Compare with registered students
            # ==============================

            for student in students:

                stored_embedding = student["face_embedding"]

                similarity = cosine_similarity(
                    current_embedding,
                    stored_embedding
                )

                if similarity > best_similarity:

                    best_similarity = similarity
                    best_match = student

            # ==============================
            # Recognition threshold
            # ==============================

            threshold = 0.70

            if best_match is not None and best_similarity >= threshold:

                name = best_match["name"]
                roll = best_match["roll"]
                department = best_match["department"]

                # Face box
                cv2.rectangle(
                    display_frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                # Student information
                cv2.putText(
                    display_frame,
                    "Recognized",
                    (x, y-70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    display_frame,
                    f"Name: {name}",
                    (x, y-45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    display_frame,
                    f"Roll: {roll}",
                    (x, y-20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    display_frame,
                    f"Department: {department}",
                    (x, y+h+25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                # ==============================
                # Mark Attendance
                # ==============================

                result = mark_attendance(
                    name,
                    roll,
                    department
                )

                # Show attendance result
                cv2.putText(
                    display_frame,
                    result,
                    (x, y+h+55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            else:

                # Unknown face
                cv2.putText(
                    display_frame,
                    "Unknown",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                cv2.rectangle(
                    display_frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 0, 255),
                    2
                )

    except Exception as e:

        # Ignore temporary recognition errors
        pass

    # Show camera
    cv2.imshow(
        "Smart Attendance System",
        display_frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()