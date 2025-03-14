import cv2
import mediapipe as mp
import pyautogui
import time
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)

cap = cv2.VideoCapture(0)

# Scroll control variables
scroll_acceleration = 3
damping_factor = 0.92
max_velocity = 30

# Hand tracking variables
prev_avg_y = {"Left": None, "Right": None}
scroll_velocity = {"Left": 0, "Right": 0}

# Tab switch variables
last_tab_switch_time = 0
cooldown = 1  # Cooldown time in seconds

# Zoom control variables
zoom_cooldown = 0.5  # Cooldown time in seconds for zoom gestures
last_zoom_time = 0
zoom_threshold = 0.05  # Threshold to detect zoom gestures

def detect_finger_extended(tip, pip):
    return tip.y < pip.y  # Finger is extended if tip is above PIP joint

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    scroll_gesture_active = {"Left": False, "Right": False}
    current_avg_y = {"Left": None, "Right": None}
    tab_switch_allowed = True  # Assume tab switching is allowed unless scrolling is detected

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label  # "Left" or "Right"
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get fingertip positions
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
            
            # Check if fingers are extended
            thumb_extended = detect_finger_extended(thumb_tip, thumb_ip)
            index_extended = detect_finger_extended(index_tip, index_pip)
            middle_extended = detect_finger_extended(middle_tip, middle_pip)
            ring_extended = detect_finger_extended(ring_tip, ring_pip)
            pinky_extended = detect_finger_extended(pinky_tip, pinky_pip)
            
            # Scroll gesture detection (all fingers extended)
            if index_extended and middle_extended and ring_extended and pinky_extended:
                scroll_gesture_active[label] = True
                tab_switch_allowed = False  # Prevent tab switching while scrolling
                current_avg_y[label] = (index_tip.y + middle_tip.y + ring_tip.y + pinky_tip.y) / 4
                
                if prev_avg_y[label] is not None:
                    delta_y = current_avg_y[label] - prev_avg_y[label]
                    scroll_velocity[label] += delta_y * scroll_acceleration
                    scroll_velocity[label] = max(-max_velocity, min(scroll_velocity[label], max_velocity))
                
                prev_avg_y[label] = current_avg_y[label]
            else:
                prev_avg_y[label] = None
                
                # Tab switch gesture detection (thumb + index extended, others folded)
                if tab_switch_allowed:
                    current_time = time.time()
                    if middle_extended and index_extended and not (thumb_extended or ring_extended or pinky_extended) and (current_time - last_tab_switch_time) > cooldown:
                        if label == "Right":
                            pyautogui.hotkey('ctrl', 'tab')  # Next tab (Right hand)
                        elif label == "Left":
                            pyautogui.hotkey('ctrl', 'shift', 'tab')  # Previous tab (Left hand)
                        last_tab_switch_time = current_time
                
                # Detect left and right pointing gesture
                if index_extended:
                    if index_tip.x < index_pip.x - 0.1:  # Index pointing left
                        pyautogui.hotkey('command', 'left')  # Go to previous page
                        time.sleep(0.5)  # Prevent multiple triggers
                    elif index_tip.x > index_pip.x + 0.1:  # Index pointing right
                        pyautogui.hotkey('command', 'right')  # Go to next page
                        time.sleep(0.5)  # Prevent multiple triggers

                # Zoom gesture detection (thumb and index finger pinch)
                current_time = time.time()
                if thumb_extended and index_extended and not (middle_extended or ring_extended or pinky_extended) and (current_time - last_zoom_time) > zoom_cooldown:
                    distance = calculate_distance(thumb_tip, index_tip)
                    if distance > zoom_threshold * 2:
                        if label =="Right":
                            pyautogui.hotkey('command', '+')  # Zoom in
                            last_zoom_time = current_time
                        elif label =="Left":
                            pyautogui.hotkey('command', '-')  # Zoom in
                            last_zoom_time = current_time
                            
    # Apply damping and perform scrolling
    for hand in ["Left", "Right"]:
        if scroll_gesture_active[hand]:
            scroll_velocity[hand] *= damping_factor
        else:
            scroll_velocity[hand] *= damping_factor ** 2
            if abs(scroll_velocity[hand]) < 1:
                scroll_velocity[hand] = 0
            prev_avg_y[hand] = None

        if abs(scroll_velocity[hand]) > 0.1:
            scroll_amount = int(abs(scroll_velocity[hand]) * 25)
            if hand == "Right":
                pyautogui.scroll(-scroll_amount)  # Right hand scrolls down
            elif hand == "Left":
                pyautogui.scroll(scroll_amount)   # Left hand scrolls up

    cv2.imshow('Hand Gesture Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()