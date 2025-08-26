import cv2
import mediapipe as mp
import math
import socket

# Socket setup to send commands to Webots
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to connect to

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def calculate_distance(landmark1, landmark2):
    return math.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)

def is_finger_extended(tip, pip, dip=None):
    if dip:
        return tip.y < pip.y and tip.y < dip.y
    else:
        return tip.x > pip.x

cap = cv2.VideoCapture(0)
with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)
        
        command = "S"  # Default: Stop
        gesture_text = "No hand"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                         mp_drawing_styles.get_default_hand_landmarks_style(),
                                         mp_drawing_styles.get_default_hand_connections_style())
                landmarks = hand_landmarks.landmark
                
                # Check finger extension
                fingers_extended = []
                fingers_extended.append(is_finger_extended(landmarks[4], landmarks[3]))
                fingers_extended.append(is_finger_extended(landmarks[8], landmarks[6], landmarks[5]))
                fingers_extended.append(is_finger_extended(landmarks[12], landmarks[10], landmarks[9]))
                fingers_extended.append(is_finger_extended(landmarks[16], landmarks[14], landmarks[13]))
                fingers_extended.append(is_finger_extended(landmarks[20], landmarks[18], landmarks[17]))
                extended_count = sum(fingers_extended)
                
                # Check pinch
                thumb_tip = landmarks[4]
                index_tip = landmarks[8]
                pinch_distance = calculate_distance(thumb_tip, index_tip)
                is_pinching = pinch_distance < 0.05
                
                # Determine command based on gesture
                if is_pinching:
                    command = "A"  # Turn left
                    gesture_text = "Pinch (Turn Left)"
                elif extended_count == 0:
                    command = "S"  # Stop
                    gesture_text = "Fist (Stop)"
                elif extended_count == 5:
                    command = "W"  # Move forward
                    gesture_text = "Open Hand (Forward)"
                else:
                    command = "D"  # Turn right
                    gesture_text = f"{extended_count} fingers (Turn Right)"
        
        # Print the command for Webots (this is the key output)
        client_socket.sendall(f"Command: {command}\n".encode())
        
        # Display gesture info on screen
        cv2.putText(image, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Gesture Control', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
