# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# import cv2
# import mediapipe as mp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock

# from ai.gesture_recognition import GestureModelDetector 
# from ai.gesture_interaction import GestureInteraction

from views.welcome_view import WelcomeScreen
from views.gallery_view import GalleryScreen
from views.opera_view import OperaScreen
from views.info_opera_view import InfoOperaScreen
from views.login_view import LoginScreen  
from views.registration_view import RegistrationScreen  
from views.add_operas_view import AddOperasScreen
from views.add_details_view import AddDetailsScreen

class MuseumApp(App):

    def build(self):
        Builder.load_file('views/welcome_screen.kv')
        Builder.load_file('views/gallery_screen.kv')
        Builder.load_file('views/opera_screen.kv')
        Builder.load_file('views/info_opera_screen.kv')
        Builder.load_file('views/login_screen.kv') 
        Builder.load_file('views/registration_screen.kv')  
        Builder.load_file('views/add_operas_screen.kv')   
        Builder.load_file('views/add_details_screen.kv')  

        sm = ScreenManager()

        sm.add_widget(WelcomeScreen(name='benvenuto'))
        sm.add_widget(GalleryScreen(name='galleria'))
        sm.add_widget(OperaScreen(name='opera'))
        sm.add_widget(InfoOperaScreen(name='info_opera'))
        sm.add_widget(LoginScreen(name='login'))  
        sm.add_widget(RegistrationScreen(name='registrazione'))  
        sm.add_widget(AddOperasScreen(name='aggiungi_opere'))  
        sm.add_widget(AddDetailsScreen(name='aggiungi_dettagli'))  

        return sm

    # def on_start(self):
    #     # Initialize gesture recognition
    #     self.mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
    #     self.gesture_detector = GestureModelDetector()
    #     self.gesture_interaction = GestureInteraction()

    #     # Initialize camera
    #     self.cap = cv2.VideoCapture(0)
        
    #     # Schedule the gesture recognition loop
    #     self.event = Clock.schedule_interval(self.ai_callback, 1.0 / 30)  # 30 FPS

    # def ai_callback(self, dt):
    #     # Capture frame
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         print("[ERROR] Non è stato possibile acquisire il frame dalla webcam.")
    #         return

    #     # Process frame
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     results = self.mp_hands.process(frame_rgb)
    #     landmarks = self.gesture_detector.extract_landmarks(results)

    #     # Detect and handle gestures
    #     if landmarks:
    #         gesture_id = self.gesture_detector.predict_gesture(landmarks)
    #         gesture_name = self.gesture_detector.class_labels[gesture_id]
    #         self.gesture_interaction.handle_gesture(gesture_name, landmarks)

    #         # Update UI or perform actions based on recognized gesture
    #         if gesture_name == "Index up" or gesture_name == "Index middle up":
    #             print(f"[INFO] Recognized gesture: {gesture_name}")
    #             # Update relevant UI elements, such as zooming or switching screens
    #         else:
    #             print("[WARNING] Gesto non riconosciuto.")

    #     # Optionally display frame for debugging
    #     cv2.imshow('Gesture Recognition', frame)

    #     # Check for exit condition to release resources
    #     if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
    #         self.stop()

    # def on_stop(self):
    #     # Cleanup resources on exit
    #     self.cap.release()
    #     cv2.destroyAllWindows()
    #     if self.event:
    #         Clock.unschedule(self.event)

if __name__ == '__main__':
    MuseumApp().run()
