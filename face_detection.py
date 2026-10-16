import cv2

# Face detection model load
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Camera open
camera = cv2.VideoCapture(0)

while True:

    # Camera থেকে frame নেওয়া
    ret, frame = camera.read()

    if not ret:
        print("Camera could not be opened!")
        break

    # Color image → Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detect
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # প্রতিটি face-এর চারপাশে rectangle
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

    # Camera window দেখানো
    cv2.imshow("Smart Attendance - Face Detection", frame)

    # Q চাপলে বন্ধ
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Camera বন্ধ
camera.release()
cv2.destroyAllWindows()q