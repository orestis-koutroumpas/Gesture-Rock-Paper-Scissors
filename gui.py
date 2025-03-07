import customtkinter as ctk
from gesture_recognition import GestureRecognizer, find_cameras, determine_winner
from PIL import Image, ImageTk
from threading import Thread
import random
import cv2
import os
import pygame
import traceback
import sys
import http.client, urllib

# Global exception handler
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = handle_exception

class GestureGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rock-Paper-Scissors Game")
        self.geometry("800x600")
        self.center_window()

        # Set the application icon
        icon_path = "assets/icon.ico"
        self.iconbitmap(icon_path)

        # Detect cameras
        self.camera_index = find_cameras()
        if self.camera_index == -1:
            print("Error: No cameras detected. Exiting.")
            self.quit()

        # Initialize gesture recognizer
        self.gesture_recognizer = GestureRecognizer(camera_index=self.camera_index)

        # Theme and appearance mode
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Initialize Pygame mixer for sound playback
        pygame.mixer.init()

        # Initialize widgets
        self.initialize_widgets()

        # Show the start screen
        self.show_start_screen()
        
        # Bind quit buttons
        self.bind("<q>", self.quit_game)
        self.bind("<Q>", self.quit_game)
        self.bind("<Escape>", self.quit_game)

    def initialize_widgets(self):
        """Initialize all widgets for the application."""
        self.label_title = ctk.CTkLabel(self, text="Rock-Paper-Scissors Game", font=("Arial", 24))
        self.start_button = self.create_button(
            text="Start Game", 
            command=self.start_game, 
            fg_color="#0078D4",
            hover_color="#005BB5"
        )
        self.quit_button = self.create_button(
            text="Quit", 
            command=self.quit_game, 
            fg_color="#FF3B30", 
            hover_color="#D32F2F"
        )
        self.camera_label = ctk.CTkLabel(self, text="Initializing camera...")
        self.feedback_label = ctk.CTkLabel(self, text="Get ready!", font=("Arial", 16))
        image_path = "assets/start_image.webp"
        start_image = ctk.CTkImage(light_image=Image.open(image_path), size=(450, 380))
        self.image_label = ctk.CTkLabel(self, image=start_image, text="")
        self.result_label = ctk.CTkLabel(self, font=("Arial", 24, "bold"))
        self.result_image_label = ctk.CTkLabel(self, text="")
        self.play_again_button = self.create_button(
            text="Play Again", 
            command=self.start_game, 
            fg_color="#0078D4", 
            hover_color="#005BB5"
        )
        self.quit_button_result = self.create_button(
            text="Quit", 
            command=self.quit_game, 
            fg_color="#FF3B30", 
            hover_color="#D32F2F"
        )
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", font=("Arial", 12))
        self.appearance_mode_switch = ctk.CTkOptionMenu(
            self, values=["System", "Light", "Dark"], command=self.change_appearance_mode
        )
        self.appearance_mode_switch.set("System")

    def create_button(self, text, command, fg_color, hover_color):
        return ctk.CTkButton(
            self,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            font=("Arial", 18, "bold"),
            corner_radius=20
        )

    def show_start_screen(self):
        self.hide_all_widgets()
        self.label_title.place(relx=0.5, rely=0.05, anchor="center")
        self.image_label.place(relx=0.5, rely=0.45, anchor="center")
        self.start_button.place(relx=0.5, rely=0.85, anchor="center")
        self.quit_button.place(relx=0.5, rely=0.92, anchor="center")

    def show_game_screen(self):
        self.hide_all_widgets()
        self.camera_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.feedback_label.pack(pady=30)
        self.appearance_mode_label.place(relx=0.70, rely=0.96, anchor="center")
        self.appearance_mode_switch.place(relx=0.88, rely=0.96, anchor="center")
        self.gesture_recognizer.reset_camera()
        if not self.gesture_recognizer.is_camera_open():
            self.camera_label.configure(text="Error: Unable to access the camera.")
            return
        self.running = True
        self.camera_thread = Thread(target=self.run_game, daemon=True)
        self.camera_thread.start()

    def show_result_screen(self, result_message, result_type):
        self.hide_all_widgets()
        if result_type == "win":
            image_path = "assets/you_win_image.webp"
            sound_path = "assets/win_sound.mp3"
        elif result_type == "lose":
            image_path = "assets/you_lose_image.webp"
            sound_path = "assets/lose_sound.wav"
        else:
            image_path = "assets/you_tie_image.webp"
            sound_path = "assets/tie_sound.mp3"
        self.result_label.configure(text=result_message)
        self.result_label.place(relx=0.5, rely=0.05, anchor="center")
        result_image = ctk.CTkImage(light_image=Image.open(image_path), size=(450, 380))
        self.result_image_label.configure(image=result_image)
        self.result_image_label.place(relx=0.5, rely=0.45, anchor="center")
        if os.path.exists(sound_path):
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        self.play_again_button.place(relx=0.5, rely=0.85, anchor="center")
        self.quit_button_result.place(relx=0.5, rely=0.92, anchor="center")

    def hide_all_widgets(self):
        for widget in self.winfo_children():
            widget.place_forget()
            widget.pack_forget()

    def start_game(self):
        self.show_game_screen()

    def run_game(self):
        try:
            self.camera_label.configure(text="")
            for count in range(3, 0, -1):
                self.feedback_label.configure(text=f"Get ready: {count}")
                ret, frame = self.gesture_recognizer.cap.read()
                if not ret:
                    self.feedback_label.configure(text="Error: Unable to access the camera.")
                    return
                frame = cv2.flip(frame, 1)
                self.update_camera_feed(frame)
                cv2.waitKey(1000)
            self.feedback_label.configure(text="Show your gesture!")
            computer_choice = random.choice(["Rock", "Paper", "Scissors"])
            user_choice = None
            while user_choice is None:
                ret, frame = self.gesture_recognizer.cap.read()
                if not ret:
                    self.feedback_label.configure(text="Error: Unable to access the camera.")
                    return
                frame = cv2.flip(frame, 1)
                user_choice = self.gesture_recognizer.detect_gesture(frame)
                self.update_camera_feed(frame)
            result_message, result_type = determine_winner(user_choice, computer_choice)
            self.feedback_label.configure(text=f"Computer: {computer_choice} | You: {user_choice}")
            cv2.waitKey(2000)
            self.show_result_screen(result_message, result_type)
            # conn = http.client.HTTPSConnection("api.pushover.net:443")
            # conn.request("POST", "/1/messages.json",
            # urllib.parse.urlencode({
            # "token": "ax3fy6y7en79jjgp5t8zs41wj83vtp",
            # "user": "uwvz7b8853rqb8wdm959dn4ihi135x",
            # "message": result_message,
            # }), { "Content-type": "application/x-www-form-urlencoded" })
            # conn.getresponse()
        finally:
            self.running = False
            self.gesture_recognizer.release_resources()

    def update_camera_feed(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))
        self.camera_label.configure(image=img)
        self.camera_label.image = img

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def quit_game(self):
        self.running = False
        if hasattr(self, 'camera_thread') and self.camera_thread.is_alive():
            self.camera_thread.join()
        self.gesture_recognizer.release_resources()
        self.quit()

    def center_window(self):
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

if __name__ == "__main__":
    app = GestureGameApp()
    app.mainloop()