import cv2
import mediapipe as mp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock


from config import FRAME_RATE, ENABLE_AI


from ai.gesture_recognition import GestureModelDetector
from ai.gesture_interaction import GestureInteraction


from app.views.welcome_view import WelcomeScreen
from app.views.gallery_view import GalleryScreen
from app.views.opera_view import OperaScreen
from app.views.info_opera_view import InfoOperaScreen
from app.views.login_view import LoginScreen  
from app.views.registration_view import RegistrationScreen  
from app.views.add_operas_view import AddOperasScreen
from app.views.add_details_view import AddDetailsScreen

class MuseumApp(App):

    def build(self):
        Builder.load_file('app/views/welcome_screen.kv')
        Builder.load_file('app/views/gallery_screen.kv')
        Builder.load_file('app/views/opera_screen.kv')
        Builder.load_file('app/views/info_opera_screen.kv')
        Builder.load_file('app/views/login_screen.kv') 
        Builder.load_file('app/views/registration_screen.kv')  
        Builder.load_file('app/views/add_operas_screen.kv')   
        Builder.load_file('app/views/add_details_screen.kv')  

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

    def on_start(self):
        if ENABLE_AI:
            # Initialize gesture recognition
            self.mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
            self.gesture_detector = GestureModelDetector()
            self.gesture_interaction = GestureInteraction()

            # Initialize camera
            self.cap = cv2.VideoCapture(0)
            
            # Schedule the gesture recognition loop
            self.event = Clock.schedule_interval(self.ai_callback, 1.0 / FRAME_RATE)  # 30 FPS

    def ai_callback(self, dt):
        if ENABLE_AI:
            # Capture frame
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Non è stato possibile acquisire il frame dalla webcam.")
                return

            # Process frame
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_hands.process(frame_rgb)
            landmarks = self.gesture_detector.extract_landmarks(results)

            # Detect and handle gestures
            if landmarks:
                gesture_id = self.gesture_detector.predict_gesture(landmarks)
                gesture_name = self.gesture_detector.class_labels[gesture_id]
                self.gesture_interaction.handle_gesture(gesture_name, landmarks)

                # Update UI or perform actions based on recognized gesture
                if gesture_name == "Index up" or gesture_name == "Index middle up":
                    print(f"[INFO] Recognized gesture: {gesture_name}")
                    # Update relevant UI elements, such as zooming or switching screens
                else:
                    print("[WARNING] Gesto non riconosciuto.")

            # Optionally display frame for debugging
            cv2.imshow('Gesture Recognition', frame)

            # Check for exit condition to release resources
            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
                self.stop()

    def on_stop(self):
        if ENABLE_AI:
            # Cleanup resources on exit
            self.cap.release()
            cv2.destroyAllWindows()
            if self.event:
                Clock.unschedule(self.event)

if __name__ == '__main__':
    MuseumApp().run()
