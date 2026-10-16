import cv2
from deepface import DeepFace

# Camera চালু
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open হচ্ছে না!")
    exit()

print("Camera started...")
print("Press 'q' to quit.")

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

        for face in faces:
            facial_area = face["facial_area"]

            x = facial_area["x"]
            y = facial_area["y"]
            w = facial_area["w"]
            h = facial_area["h"]

            # Face-এর চারপাশে rectangle
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
        print("Error:", e)

    cv2.imshow("Face Recognition Test", frame)

    # q চাপলে বন্ধ হবে
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

