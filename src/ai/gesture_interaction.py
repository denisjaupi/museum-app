import collections
import pyautogui
import cv2
import mediapipe as mp
import gesture_recognition as gr
import math
import time

class GestureInteraction:

    def __init__(self):
        # Ottieni dimensioni dello schermo
        self.screen_width, self.screen_height = pyautogui.size()
        # Coda per memorizzare le ultime 5 posizioni del dito
        self.pointer_positions = collections.deque(maxlen=5)


        # Timer per bloccare i gesti opposti per un breve periodo
        self.last_zoom_time = 0
        self.zoom_cooldown = 1  # 1 secondo di cooldown tra i gesti opposti
        self.last_position = None  # Posizione dell'immagine

################################################################################


    def calculate_distance(self, point1, point2):
        """Calcola la distanza euclidea tra due punti 3D."""
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


    def move_mouse(self, index_finger_coords):
        """Muove il puntatore del mouse usando le coordinate della punta dell'indice."""
        # Estrarre le coordinate X e Y della punta dell'indice
        index_x = index_finger_coords.x
        index_y = index_finger_coords.y

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


    def scroll(self, current_position):
        """
        Simula lo scorrimento in base al movimento verticale e orizzontale della mano.
        """
        current_x, current_y = current_position
        if self.last_position is not None:
            last_x, last_y = self.last_position
            delta_x = last_x - current_x  # Movimento orizzontale
            delta_y = last_y - current_y  # Movimento verticale

            # Ignora piccoli movimenti per evitare scorrimenti indesiderati
            if abs(delta_y) > 5:
                pyautogui.scroll(int(delta_y))  # Scroll verticale
            if abs(delta_x) > 5:
                pyautogui.hscroll(int(delta_x))  # Scroll orizzontale

        # Aggiorna l'ultima posizione della punta dell'indice
        self.last_position = current_position


################################################################################


    def indexUp(self, landmarks):

        index_finger_tip = landmarks[8]  # Punta dell'indice

        # Le coordinate di MediaPipe sono normalizzate (0-1), quindi possiamo utilizzarle direttamente
        self.move_mouse((index_finger_tip))


    def indexMiddleUp(self, landmarks):

        index_finger_tip = landmarks[8] 
        
        current_position = (int(index_finger_tip.x * self.screen_width), int(index_finger_tip.y * self.screen_height))
        self.scroll(current_position)
        

    def zoomIn(self, landmarks):
        """Calcola il vettore di zoom in tra pollice e indice."""
        current_time = time.time()
        
        # Controlla se è passato abbastanza tempo dall'ultimo zoom out
        if current_time - self.last_zoom_time < self.zoom_cooldown:
            print("Aspetta prima di fare uno zoom in.")
            return

        thumb_tip = landmarks[4]  # Punta del pollice
        index_finger_tip = landmarks[8]  # Punta dell'indice

        # Calcola la distanza tra le due punte
        distance = self.calculate_distance(thumb_tip, index_finger_tip)

        # Esegui il zoom in in base alla distanza
        print(f"Zoom in - Distanza tra le dita: {distance}")

        # Imposta il timer per evitare il gesto opposto immediato
        self.last_zoom_time = current_time



    def zoomOut(self, landmarks):
        """Calcola il vettore di zoom out tra pollice e indice."""
        current_time = time.time()
        
        # Controlla se è passato abbastanza tempo dall'ultimo zoom in
        if current_time - self.last_zoom_time < self.zoom_cooldown:
            print("Aspetta prima di fare uno zoom out.")
            return

        thumb_tip = landmarks[4]  # Punta del pollice
        index_finger_tip = landmarks[8]  # Punta dell'indice

        # Calcola la distanza tra le due punte
        distance = self.calculate_distance(thumb_tip, index_finger_tip)

        # Esegui il zoom out in base alla distanza (ad esempio, puoi scalare un'immagine)
        print(f"Zoom out - Distanza tra le dita: {distance}")

        # Imposta il timer per evitare il gesto opposto immediato
        self.last_zoom_time = current_time


################################################################################


    def handle_gesture(self, gesture_name, landmarks):
        """Gestisci l'interazione basata sul gesto riconosciuto."""
        if gesture_name == "Indice alzato":
            self.indexUp(landmarks)
        elif gesture_name == "Indice e medio alzati":
            self.indexMiddleUp(landmarks)
        elif gesture_name == "Zoom in":
            self.zoomIn(landmarks)
        elif gesture_name == "Zoom out":
            self.zoomOut(landmarks)


################################################################################


def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)

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


        ############################################################################################

        # Se sono presenti landmark, procedi al riconoscimento dei gesti
        if landmarks:
            # Prevedi il gesto usando il modello addestrato
            gesture_id = gesture_detector.predict_gesture(landmarks)
            gesture_name = gesture_detector.class_labels.get(gesture_id)

            # Verifica i gesti riconosciuti dal modello e gestisci le azioni
            if gesture_name == "Indice e medio alzati":
            # or gesture_name == "Zoom in" or gesture_name == "Zoom out": 
                # Gestisci i gesti tranne l'indice alzato
                gesture_interaction.handle_gesture(gesture_name, landmarks)
            else:
                # Se non viene riconosciuto nessuno degli altri gesti, controlla se l'indice è alzato
                if gesture_detector.is_index_finger_up(landmarks): 
                    # Gestisci il movimento del cursore
                    gesture_name = "Indice alzato"
                    gesture_interaction.indexUp(landmarks)
                else:
                    gesture_name = "Gesto non riconosciuto"
        
        ############################################################################################


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
