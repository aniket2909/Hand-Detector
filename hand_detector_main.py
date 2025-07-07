import cv2
import mediapipe as mp
import webbrowser
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

chrome_open = False

 # remembering last action so that chrome does not keep opening more tabs as the hand keeps being detected by the camera
last_action = None

def fingers_up(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []

    # for recognizing fingers from the landmarks + when they open and close
    for tip in tips:
	    # finger up
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
	# finger down
        else:
            fingers.append(0)
    return fingers

# function to open chrome upon detecting open palm
def open_chrome():
    global chrome_open
    if not chrome_open:
        webbrowser.open("https://www.google.com")
        chrome_open = True

# function to close chrome on detecting closed palm / fist
def close_chrome():
    global chrome_open
    if chrome_open:
        os.system("taskkill /F /IM chrome.exe")
        chrome_open = False

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gesture_text = "No Gesture"

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        fingers = fingers_up(hand_landmarks)
        total_fingers = sum(fingers)

	# excluding the thumb in total_fingers as it hindered the recognition of left hand
        if total_fingers == 4:
            detected_gesture = "Open Palm"
            if detected_gesture != last_action:
                open_chrome()
                last_action = detected_gesture
        elif total_fingers == 0:
            detected_gesture = "Closed Palm"
            if detected_gesture != last_action:
                close_chrome()
                last_action = detected_gesture
        else:
            detected_gesture = "Unknown"

        gesture_text = detected_gesture
    else:
        last_action = None  # if no hand detected

    cv2.putText(img, f"Gesture: {gesture_text}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Hand Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
