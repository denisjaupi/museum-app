import cv2
import os
import mediapipe as mp
import numpy as np
import joblib

# TODO:
# Da aggiungere una nuova classe per i gesti non classificati.

class GestureModelDetector:
    def __init__(self):
        self.class_labels = {
            0: "Index up",
            1: "Index middle up",
            2: "Zoom in"
        }
        self.model_path =  os.path.join(os.path.dirname(__file__), 'model', 'gesture_recognition_model.pkl')

    def load_model(self, model_path):
        """Carica il modello addestrato."""
        model = joblib.load(model_path)
        return model

    def predict_gesture(self, landmarks):
        """Prevede il gesto basato sulle coordinate dei landmark."""
        model = self.load_model(self.model_path)
        coordinates = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
        return model.predict([coordinates])[0]
    
    def extract_landmarks(self, results):
        """Estrae le coordinate dei landmark."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                return hand_landmarks.landmark
            
    def is_index_finger_up(self, landmarks):
        """Riconosce se il dito indice è alzato basato sui landmarks, considerando l'orientamento della mano."""
        index_finger_tip = landmarks[8]  # Punta dell'indice
        index_finger_mid = landmarks[6]  # Punto medio dell'indice
        middle_finger_tip = landmarks[12]  # Punta del medio
        wrist = landmarks[0]  # Polso

        # Verifica l'orientamento della mano:
        # Se il polso è sotto il punto medio dell'indice, la mano è verso l'alto (normale).
        if wrist.y < index_finger_mid.y:
            # Mano rivolta verso l'alto: l'indice è considerato alzato se la punta è sopra il punto medio
            is_index_extended = index_finger_tip.y > index_finger_mid.y
            is_above_other_fingers = index_finger_tip.y > middle_finger_tip.y
        else:
            # Mano rivolta verso il basso: l'indice è alzato se la punta è sotto il punto medio
            is_index_extended = index_finger_tip.y < index_finger_mid.y
            is_above_other_fingers = index_finger_tip.y < middle_finger_tip.y

        # L'indice è considerato alzato se è esteso e sopra il medio, in base all'orientamento della mano
        return is_index_extended and is_above_other_fingers



    
def main():
    # Inizializza MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1, min_tracking_confidence=0.5)

    # Carica il modello addestrato
    trainer = GestureModelDetector()
    model = trainer.load_model('src/ai/model/gesture_recognition_model.pkl')

    # Inizializza la webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Non è stato possibile acquisire il frame dalla webcam.")
            break

        # Converti il frame in RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Disegna le mani e riconosci i gesti
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # # Estrai le coordinate delle mani
                hand_landmarks = trainer.extract_landmarks(results)
                
                # Prevedi il gesto
                gesture_id = trainer.predict_gesture(hand_landmarks)
                gesture_name = trainer.class_labels[gesture_id]
                
                # Disegna i landmarks
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Mostra il nome del gesto
                cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Mostra il frame
        cv2.imshow('Gesture Recognition', frame)

        # Esci se premi ESC
        if cv2.waitKey(1) & 0xFF == 27:  # 27 è il codice ASCII per ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
