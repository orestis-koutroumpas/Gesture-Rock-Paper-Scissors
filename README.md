# Gesture Rock-Paper-Scissors Game

This interactive Rock-Paper-Scissors game allows you to play against the computer using hand gestures. The application utilizes MediaPipe for gesture recognition and a custom Tkinter GUI built with customtkinter for a seamless user interface. The game provides real-time feedback with both visual and haptic feedback. The camera tracks your hand gestures, and you can enjoy the game with sound effects and on-screen messages.

## Features

- **Gesture Recognition**: Play Rock-Paper-Scissors using hand gestures captured by your camera.
- **Custom Tkinter GUI**: Beautiful and responsive UI with support for different appearance modes (Light, Dark, and System modes).
- **Real-time Feedback**: Get visual feedback for the game, including win, loss, or tie messages.
- **Camera Access**: Automatically detects internal or external cameras for gesture recognition.
- **Sound Effects**: Enjoy sound effects when you win, lose, or tie in the game.
- **Start Screen**: An introductory screen with options to start the game or quit.

## Technology Used
- MediaPipe: For hand gesture recognition using 21 key points (landmarks) on the hand.
- OpenCV: For capturing video from the camera.
- CustomTkinter: For the GUI framework that allows for a modern, customizable user interface.
- PushOver API: For providing real-time push notifications to mobile devices and smartwatches.
- Pygame: To integrate sound effects based on the game outcome.

## Requirements

- Python 3.x
- `customtkinter`: A modern and customizable tkinter library.
- `opencv-python`: For handling video capture from the camera.
- `pygame`: For sound effects.
- `mediapipe`: For hand gesture recognition.
- `Pillow`: For image processing.

To install the required libraries, you can use the following command:

                pip install customtkinter opencv-python pygame mediapipe pillow

## How to Run

### 1. Clone this repository to your local machine:

git clone https://github.com/your-username/gesture-rock-paper-scissors.git

### 2. Navigate to the project directory:

        cd gesture-rock-paper-scissors-main

### 3. Run the main application script:

python gui.py

### 4. Follow the on-screen instructions to play the game using hand gestures.

## Game Instructions

- Start the Game: Once the game starts, the camera will initialize, and a countdown will be displayed on the screen.
- Perform a Gesture: When the countdown reaches "Show your gesture!", perform one of the three gestures (Rock, Paper, or Scissors) in front of the camera.
- Result Display: The result will be displayed based on your gesture and the computer's random choice.
- Feedback: Visual, sound, and haptic feedback will be provided based on the outcome of the round.
- Play Again or Quit: You can play again or quit at any time.

## Game Mechanics
The game follows the classic rules of Rock-Paper-Scissors:

- Rock beats Scissors.
- Scissors beats Paper.
- Paper beats Rock.

The computer's choice is randomly selected, and the game will provide feedback about whether you won, lost, or tied. The system also uses hand landmarks for gesture recognition:

- Rock: All fingers are curled into a fist.
- Paper: All fingers are fully extended.
- Scissors: Only the index and middle fingers are extended.

## Acknowledgments
This project was developed by:

- Dimitris Gkounelas
- Ioannis Nikolaos Theodorou
- Orestis Koutroumpas
- Konstantinos Toutounas

The game integrates advanced technologies such as computer vision, haptic feedback, and real-time notifications to enhance the interactive experience. The use of MediaPipe for gesture recognition and PushOver API for real-time feedback makes the game a cutting-edge project that combines fun and technology.
