import cv2

# Open the camera
camera = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = camera.read()

    if not ret:
        print("Camera could not be opened!")
        break

    # Show camera video
    cv2.imshow("Smart Attendance System", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera
camera.release()
cv2.destroyAllWindows()