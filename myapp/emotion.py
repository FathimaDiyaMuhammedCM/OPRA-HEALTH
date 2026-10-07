# import cv2
# from fer import FER
#
# def emotion_detector_fer():
#     # Initialize the emotion detector
#     detector = FER(mtcnn=True)  # You can set mtcnn=False for faster but less accurate detection
#
#     # Start the webcam
#     cap = cv2.VideoCapture(0)
#
#
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to grab frame.")
#             break
#
#         # Detect emotions
#         results = detector.detect_emotions(frame)
#
#         for result in results:
#             # Get bounding box
#             (x, y, w, h) = result["box"]
#             # Get emotions dictionary
#             emotions = result["emotions"]
#             # Get dominant emotion
#             dominant_emotion = max(emotions, key=emotions.get)
#
#             # Draw rectangle around face
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             # Put text above the rectangle
#             cv2.putText(frame, f"{dominant_emotion} ({emotions[dominant_emotion]:.2f})",
#                         (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
#
#         # Show the frame
#         cv2.imshow("FER - Emotion Detection", frame)
#
#         # Press 'q' to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release resources
#     cap.release()
#     cv2.destroyAllWindows()
#
# # Run the emotion detector
#
# emotion_detector_fer()

import os
import django
import cv2
from fer import FER
import datetime

# ✅ Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mithra.settings')  # <-- change this
django.setup()

# ✅ Import your model
from myapp.models import Facial_emotion, Women  # <-- change yourappname

def emotion_detector_fer():
    # Initialize the emotion detector
    detector = FER(mtcnn=True)

    # Start the webcam
    cap = cv2.VideoCapture(0)

    # Create a directory for saved photos
    os.makedirs("captured_faces", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Detect emotions
        results = detector.detect_emotions(frame)

        for result in results:
            (x, y, w, h) = result["box"]
            emotions = result["emotions"]
            dominant_emotion = max(emotions, key=emotions.get)

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{dominant_emotion} ({emotions[dominant_emotion]:.2f})",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

            # Save cropped face photo
            face_crop = frame[y:y + h, x:x + w]
            filename = f"emotion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join("captured_faces", filename)
            cv2.imwrite(filepath, face_crop)

            print(f"Saved image: {filename} | Emotion: {dominant_emotion}")

            # ✅ Save to Django database
            try:
                # Get the WOMEN record (example: WOMEN with id=1)
                woman = Women.objects.get(id=1)  # <-- Change ID dynamically if needed

                Facial_emotion.objects.create(
                    date=datetime.date.today(),
                    time=datetime.datetime.now().time(),
                    emotion=dominant_emotion,
                    photo=filepath,
                    WOMEN=woman
                )

                print("✅ Saved emotion and photo to database")

            except Exception as e:
                print("❌ Error saving to DB:", e)

        # Show the webcam feed
        cv2.imshow("FER - Emotion Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera
    cap.release()
    cv2.destroyAllWindows()


# Run the detector
emotion_detector_fer()
