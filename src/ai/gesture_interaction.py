import collections
import pyautogui
import cv2
import mediapipe as mp
import gesture_recognition as gr

class GestureInteraction:
    def __init__(self):
        # Ottieni dimensioni dello schermo
        self.screen_width, self.screen_height = pyautogui.size()
        # Coda per memorizzare le ultime 5 posizioni del dito
        self.pointer_positions = collections.deque(maxlen=5)

    def move_mouse(self, index_finger_coords):
        """Muove il puntatore del mouse usando le coordinate della punta dell'indice."""
        # Estrarre le coordinate X e Y della punta dell'indice
        index_x, index_y = index_finger_coords

        # Scala le coordinate in base alla risoluzione dello schermo
        mouse_x = int(index_x * self.screen_width)
        mouse_y = int(index_y * self.screen_height)

        # Aggiungi la posizione corrente alla coda
        self.pointer_positions.append((mouse_x, mouse_y))

        # Calcola la posizione smussata
        smoothed_x = int(sum(pos[0] for pos in self.pointer_positions) / len(self.pointer_positions))
        smoothed_y = int(sum(pos[1] for pos in self.pointer_positions) / len(self.pointer_positions))

        # Muove il mouse alla posizione smussata
        pyautogui.moveTo(smoothed_x, smoothed_y)


    def handle_gesture(self, gesture_name, landmarks):
        """Gestisci l'interazione basata sul gesto riconosciuto."""
        if gesture_name == "Indice alzato":
            # Coordinate della punta dell'indice (landmark[8] in MediaPipe Hands)
            index_finger_tip = landmarks[8]  # 8 è la punta dell'indice in MediaPipe

            # Le coordinate di MediaPipe sono normalizzate (0-1), quindi possiamo utilizzarle direttamente
            self.move_mouse((index_finger_tip.x, index_finger_tip.y))



def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

    # Inizializza il riconoscimento dei gesti e l'interazione
    gesture_detector = gr.GestureModelDetector()
    gesture_interaction = GestureInteraction()

    # Inizializza la webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Non è stato possibile acquisire il frame dalla webcam.")
            break

        # Converti il frame in RGB per MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Estrai i landmark delle mani dal risultato
        landmarks = gesture_detector.extract_landmarks(results)

        # Se sono presenti landmark, procedi al riconoscimento dei gesti
        if landmarks:
            # Prevedi il gesto
            gesture_id = gesture_detector.predict_gesture(landmarks)
            gesture_name = gesture_detector.class_labels.get(gesture_id, "Gesto sconosciuto")

            # Gestisci l'interazione in base al gesto riconosciuto
            gesture_interaction.handle_gesture(gesture_name, landmarks)

            # Disegna i landmarks sul frame e visualizza il nome del gesto
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Mostra il nome del gesto riconosciuto
            cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Mostra il frame
        cv2.imshow('Gesture Recognition', frame)

        # Esci dal ciclo se premi ESC
        if cv2.waitKey(1) & 0xFF == 27:  # 27 è il codice ASCII per ESC
            break

    # Rilascia la webcam e chiudi tutte le finestre
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
