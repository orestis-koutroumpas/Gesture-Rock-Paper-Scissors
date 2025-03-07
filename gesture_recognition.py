import cv2
import mediapipe as mp

class GestureRecognizer:
    def __init__(self, camera_index=0):
        """Initialize the gesture recognizer with MediaPipe and camera."""
        self.camera_index = camera_index
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = None
        self.initialize_camera()

    def initialize_camera(self):
        """Initialize the camera."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Error: Unable to access the camera.")
            self.cap = None

    def reset_camera(self):
        """Reinitialize the camera after releasing resources."""
        self.release_resources()
        self.initialize_camera()

    def is_camera_open(self):
        """Check if the camera is open and accessible."""
        return self.cap is not None and self.cap.isOpened()

    def detect_gesture(self, frame):
        """Detect the gesture from the camera frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                return self.recognize_gesture(hand_landmarks.landmark)
        return None

    def recognize_gesture(self, landmarks):
        """Recognize the gesture based on hand landmarks."""
        fingers = []
        fingers.append(landmarks[4].x < landmarks[3].x)  # Thumb
        for tip_idx, dip_idx in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            fingers.append(landmarks[tip_idx].y < landmarks[dip_idx].y)  # Finger extended if tip is above dip

        # Rock: All fingers folded
        if not any(fingers):
            return "Rock"
        # Paper: All fingers extended
        elif all(fingers):
            return "Paper"
        # Scissors: Only index and middle fingers extended
        elif fingers[1] and fingers[2] and not fingers[0] and not fingers[3] and not fingers[4]:
            return "Scissors"
        return None

    def release_resources(self):
        """Release camera and MediaPipe resources."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

def find_cameras():
    """Searches for internal and external cameras and returns the first available one."""
    internal_indices = [0, 1]  # Possible indices for internal cameras
    external_indices = list(range(2, 10))  # Possible indices for external cameras

    # Search for internal cameras
    for index in internal_indices:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"Internal camera found at index {index}")
            cap.release()
            return index
        else:
            print(f"No internal camera at index {index}")

    # Search for external cameras
    for index in external_indices:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"External camera found at index {index}")
            cap.release()
            return index
        else:
            print(f"No external camera at index {index}")

    # If no camera is found
    print("Error: No cameras detected.")
    return -1

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!", "tie"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        return "You win!", "win"
    else:
        return "You lose!", "lose"