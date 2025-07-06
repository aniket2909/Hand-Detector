import cv2
import mediapipe as mp
import time
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Path to Chrome executable (update as needed for your OS)
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_open = False

# Start webcam
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for natural (mirror) interaction
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw hand landmarks and trigger action
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if not chrome_open:
                os.startfile(chrome_path)
                chrome_open = True
                time.sleep(2)  # Prevent rapid re-triggering
        else:
            if chrome_open:
                os.system('taskkill /IM chrome.exe')
                chrome_open = False
                time.sleep(2)  # Prevent rapid re-triggering

        cv2.imshow("Hand Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()