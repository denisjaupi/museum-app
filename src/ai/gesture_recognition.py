import cv2
import mediapipe as mp
import numpy as np
import joblib

# TODO:
# Da migliorare le classi csv catturando nuovi dati. 
# Zoom out è problematico e si confonde con indice alzato.

class GestureModelDetector:
    def __init__(self):
        self.class_labels = {
            0: "Indice alzato",
            1: "Indice e medio alzati",
            2: "Zoom in",
            3: "Zoom out"
        }
        self.model_path =  'src/ai/model/gesture_recognition_model.pkl'

    def load_model(self, model_path):
        """Carica il modello addestrato."""
        return joblib.load(model_path)

def main():
    # Inizializza MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

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
                # Estrai le coordinate delle mani
                landmarks = hand_landmarks.landmark
                coordinates = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()

                # Prevedi il gesto
                gesture_id = model.predict([coordinates])[0]
                gesture_name = trainer.class_labels.get(gesture_id, "Gesto sconosciuto")

                # Disegna i landmarks
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
