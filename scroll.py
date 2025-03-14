import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_handedness = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Scroll control variables
scroll_acceleration = 3
damping_factor = 0.92
max_velocity = 30

# Hand tracking variables
prev_avg_y = {"Left": None, "Right": None}
scroll_velocity = {"Left": 0, "Right": 0}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    scroll_gesture_active = {"Left": False, "Right": False}
    current_avg_y = {"Left": None, "Right": None}

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label  # "Left" or "Right"
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get fingertip positions
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

            # Check if fingers are extended
            index_extended = index_tip.y < index_pip.y
            middle_extended = middle_tip.y < middle_pip.y
            ring_extended = ring_tip.y < ring_pip.y
            pinky_extended = pinky_tip.y < pinky_pip.y

            # Scroll gesture detection (all fingers extended)
            if index_extended and middle_extended and ring_extended and pinky_extended:
                scroll_gesture_active[label] = True
                current_avg_y[label] = (index_tip.y + middle_tip.y + ring_tip.y + pinky_tip.y) / 4

                if prev_avg_y[label] is not None:
                    delta_y = current_avg_y[label] - prev_avg_y[label]
                    scroll_velocity[label] += delta_y * scroll_acceleration
                    scroll_velocity[label] = max(-max_velocity, min(scroll_velocity[label], max_velocity))

                prev_avg_y[label] = current_avg_y[label]
            else:
                prev_avg_y[label] = None

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

    cv2.imshow('Hand Gesture Scrolling', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
