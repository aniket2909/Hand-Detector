import cv2
import mediapipe as mp
import time
import os
import platform

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Track Chrome state
chrome_open = False

def count_visible_fingers(hand_landmarks):
    """
    Count how many fingers are extended/visible
    Returns the number of fingers that are up
    """
    finger_count = 0
    
    # Thumb - check if tip is to the right of the joint below it
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        finger_count += 1
    
    # Other fingers - check if tip is above the joint below it
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
    finger_joints = [6, 10, 14, 18]  # Corresponding joints
    
    for tip, joint in zip(finger_tips, finger_joints):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[joint].y:
            finger_count += 1
    
    return finger_count

def is_full_palm_visible(hand_landmarks):
    """
    Check if the full palm is visible by ensuring all 5 fingers are detected
    """
    finger_count = count_visible_fingers(hand_landmarks)
    return finger_count == 5  # All 5 fingers must be visible

def open_chrome():
    """
    Open Chrome browser based on the operating system
    """
    system = platform.system()
    
    if system == "Windows":
        # Checking all common Chrome locations on Windows
        # It's one of the edge cases and this one caused the program to not work as intended initially,.
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\Public\Desktop\Google Chrome.lnk"
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                os.startfile(path)
                return True
        # If no path found, try generic command
        os.system("start chrome")
        
    elif system == "Darwin":  # macOS
        os.system("open -a 'Google Chrome'")
        
    elif system == "Linux":
        os.system("google-chrome")
    
    return True

def close_chrome():
    """
    Close Chrome browser based on the operating system
    """
    system = platform.system()
    
    if system == "Windows":
        os.system('taskkill /IM chrome.exe /F')
    elif system == "Darwin":  # macOS
        os.system("pkill -f 'Google Chrome'")
    elif system == "Linux":
        os.system("pkill chrome")

# Start webcam
print("Starting camera... Show your open palm (all 5 fingers) to open Chrome")
print("Hide your palm or close your hand to close Chrome")
print("Press 'q' to quit")

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera")
            break

        # Flip the frame so it acts like a mirror
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        
        # Convert color for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Check if full palm is visible
        full_palm_detected = False
        finger_count = 0
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Count fingers and check if full palm is visible
                finger_count = count_visible_fingers(hand_landmarks)
                full_palm_detected = is_full_palm_visible(hand_landmarks)
        
        # Display finger count and status on screen
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if full_palm_detected:
            cv2.putText(frame, "FULL PALM DETECTED", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Chrome: OPENING", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Show all 5 fingers", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if chrome_open:
                cv2.putText(frame, "Chrome: CLOSING", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Control Chrome based on palm detection
        if full_palm_detected:
            if not chrome_open:
                print("Full palm detected! Opening Chrome...")
                open_chrome()
                chrome_open = True
                time.sleep(2)  # Prevent rapid triggering
        else:
            if chrome_open:
                print("Palm hidden! Closing Chrome...")
                close_chrome()
                chrome_open = False
                time.sleep(2)  # Prevent rapid triggering

        # Show the camera feed
        cv2.imshow("Palm Detector - Press 'q' to quit", frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()

# Close Chrome if it's still open when program exits
if chrome_open:
    close_chrome()
    print("Program ended - Chrome closed")