import cv2
import os
import json
from deepface import DeepFace

# ==============================
# Student Information
# ==============================

name = input("Enter Student Name: ")
roll = input("Enter Student Roll: ")
department = input("Enter Department: ")

# Student data folder
os.makedirs("students", exist_ok=True)

print("\nStarting camera...")
print("Look at the camera.")
print("Press SPACE to capture your face.")
print("Press Q to cancel.\n")

# ==============================
# Camera
# ==============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open হচ্ছে না!")
    exit()

captured = False

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera থেকে frame নেওয়া যাচ্ছে না!")
        break

    # Face detection
    try:

        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            enforce_detection=False
        )

        # Draw face box
        for face in faces:

            facial_area = face["facial_area"]

            x = facial_area["x"]
            y = facial_area["y"]
            w = facial_area["w"]
            h = facial_area["h"]

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    except Exception as e:
        print("Face detection error:", e)

    # Instructions on screen
    cv2.putText(
        frame,
        "Press SPACE to capture",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to cancel",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("Student Registration", frame)

    key = cv2.waitKey(1) & 0xFF

    # SPACE চাপলে face capture
    if key == 32:

        print("\nCapturing face...")

        # Face encoding/embedding তৈরি
        try:

            embedding_result = DeepFace.represent(
                img_path=frame,
                model_name="Facenet512",
                detector_backend="opencv",
                enforce_detection=True
            )

            if len(embedding_result) == 0:
                print("No face detected!")
                continue

            # প্রথম face-এর embedding
            face_embedding = embedding_result[0]["embedding"]

            # Student information
            student_data = {
                "name": name,
                "roll": roll,
                "department": department,
                "face_embedding": face_embedding
            }

            # File name
            file_path = f"students/{roll}.json"

            # Save student data
            with open(file_path, "w") as file:
                json.dump(student_data, file, indent=4)

            print("\n================================")
            print("Student registered successfully!")
            print("================================")
            print("Name       :", name)
            print("Roll       :", roll)
            print("Department :", department)
            print("Saved file :", file_path)

            captured = True
            break

        except Exception as e:
            print("\nFace registration failed!")
            print("Error:", e)

    # Q চাপলে cancel
    elif key == ord("q"):
        print("\nRegistration cancelled.")
        break


# Camera বন্ধ
cap.release()
cv2.destroyAllWindows()

if captured:
    print("\nRegistration complete.")

