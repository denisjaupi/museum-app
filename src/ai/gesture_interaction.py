import collections
import time
import pyautogui
import cv2
import mediapipe as mp
import gesture_recognition as gr
from utils import zooming_gesture as zg


class GestureInteraction:

    def __init__(self, smoothing_factor=5):
        # Ottieni dimensioni dello schermo
        self.screen_width, self.screen_height = pyautogui.size()
        # Coda per memorizzare le ultime 5 posizioni del dito
        self.pointer_positions = collections.deque(maxlen=smoothing_factor)

        self.last_position = None  # Posizione dell'immagine
        
        self.last_move_time = time.time() # Timer per il movimento del mouse

        # Aggiungi ZoomingController per gestire lo zoom
        self.zoom_controller = zg.ZoomingController()
        self.image = None  # Immagine da zoomare


    def set_image(self, image):
        """Imposta l'immagine su cui applicare lo zoom."""
        self.image = image

################################################################################

    def smooth(self, new_position):
        self.pointer_positions.append(new_position)
        avg_x = sum(pos[0] for pos in self.pointer_positions) / len(self.pointer_positions)
        avg_y = sum(pos[1] for pos in self.pointer_positions) / len(self.pointer_positions)
        return int(avg_x), int(avg_y)


    def move_mouse(self, index_finger_coords):
        current_time = time.time()
        if current_time - self.last_move_time < 0.05:  # 50 ms di intervallo
            return 

        # Scala le coordinate della punta dell'indice rispetto alla risoluzione dello schermo
        mouse_x = int(index_finger_coords.x * self.screen_width)
        mouse_y = int(index_finger_coords.y * self.screen_height)
        smoothed_x, smoothed_y = self.smooth((mouse_x, mouse_y))

        pyautogui.moveTo(smoothed_x, smoothed_y)

        # Aggiorna l'ultima posizione
        self.last_position = (smoothed_x, smoothed_y)


    def scroll(self, index_finger_coords):
        # Scala le coordinate della punta dell'indice
        scroll_x = int(index_finger_coords.x * self.screen_width)
        scroll_y = int(index_finger_coords.y * self.screen_height)

        if self.last_position is not None:
            last_x, last_y = self.last_position
            delta_x = last_x - scroll_x 
            delta_y = last_y - scroll_y  

            scroll_sensitivity = 1
            # Ignora piccoli movimenti (10 pixel) per evitare scorrimenti indesiderati
            if abs(delta_y) > 10:
                pyautogui.scroll(int(delta_y * scroll_sensitivity))  # Scroll verticale
            if abs(delta_x) > 10:
                pyautogui.hscroll(int(delta_x * scroll_sensitivity))  # Scroll orizzontale

        # Aggiorna l'ultima posizione
        self.last_position = self.smooth((scroll_x, scroll_y))


    def click(self, index_finger_coords):
        current_time = time.time()

        # Scala le coordinate della punta dell'indice
        mouse_x, mouse_y = self.smooth((int(index_finger_coords.x * self.screen_width),
                                        int(index_finger_coords.y * self.screen_height)))

        # Controlla se il mouse è rimasto fermo nella stessa posizione
        if self.last_position:
            last_x, last_y = self.last_position

            # Consideriamo il mouse fermo se la differenza è minore di una soglia, 5 pixel
            if abs(mouse_x - last_x) < 5 and abs(mouse_y - last_y) < 5:
                # Se il mouse è fermo per più di 3 secondi, esegui il click
                if current_time - self.last_move_time > 2.5:
                    pyautogui.click() 
                    print("Click eseguito!")
            else:
                # Se il mouse si è mosso, aggiorna il timer
                self.last_move_time = current_time

        # Aggiorna l'ultima posizione del mouse
        self.last_position = (mouse_x, mouse_y)


################################################################################


    def indexUp(self, landmarks):
        index_finger_tip = landmarks[8]  # Punta dell'indice
        self.move_mouse(index_finger_tip)
        self.click(index_finger_tip)


    def indexMiddleUp(self, landmarks):
        index_finger_tip = landmarks[8] 
        self.scroll(index_finger_tip)


    def zoomGesture(self, landmarks):
        """Attiva lo zoom solo se è presente un'immagine a schermo intero."""
        if self.image is not None:  # Verifica se l'immagine è impostata
            if landmarks:
                index_finger_tip = landmarks[8]
                thumb_tip = landmarks[4]

                # Ottieni le dimensioni dell'immagine
                image_height, image_width = self.image.shape[:2]

                # Calcola la distanza tra indice e pollice
                current_distance = self.zoom_controller.calculate_distance(
                    thumb_tip, index_finger_tip, image_width, image_height)

                # Processa lo zoom con la logica implementata
                self.zoom_controller.process_zoom(current_distance)

                # Applica il fattore di zoom all'immagine se esiste un'immagine
                zoomed_image = self.zoom_controller.apply_zoom(self.image)
                self.image = zoomed_image
            else:
                # Resetta lo stato dello zoom se non vengono rilevate mani
                self.zoom_controller.reset_zoom()
        else:
            print("Zoom non attivato: nessuna immagine a schermo.")


################################################################################


    def handle_gesture(self, gesture_name, landmarks):
        """Gestisci l'interazione basata sul gesto riconosciuto."""
        if gesture_name == "Indice alzato" or gesture_name == "Indice ancora alzato":
            self.indexUp(landmarks)
        elif gesture_name == "Indice e medio alzati":
            self.indexMiddleUp(landmarks)
        elif gesture_name == "Zoom in" or gesture_name == "Zoom out":
            self.zoomGesture(landmarks)

################################################################################


def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)

    # Inizializza il riconoscimento dei gesti e l'interazione
    gesture_detector = gr.GestureModelDetector()
    gesture_interaction = GestureInteraction()

    # Carica un'immagine da visualizzare e zoomare (schermo intero)
    image_path = 'IMG_Test.JPG'  # Sostituisci con il percorso reale dell'immagine
    image = cv2.imread(image_path)

    # Imposta l'immagine su GestureInteraction per lo zoom
    if image is not None:
        gesture_interaction.set_image(image)
        print("[INFO] Immagine caricata con successo per lo zoom.")
    else:
        print("[ERROR] Non è stato possibile caricare l'immagine.")
    
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
            gesture_name = gesture_detector.class_labels[gesture_id]

            # Verifica i gesti riconosciuti dal modello e gestisci le azioni
            if gesture_name == "Indice alzato" or\
                 gesture_name == "Indice e medio alzati" or\
                     gesture_name == "Zoom in" or gesture_name == "Zoom out":
                gesture_interaction.handle_gesture(gesture_name, landmarks)
            else:
                # Se non viene riconosciuto nessuno degli altri gesti, 
                # controlla se l'indice è alzato per il movimento del mouse
                if gesture_detector.is_index_finger_up(landmarks): 
                    gesture_name = "Indice ancora alzato"
                    gesture_interaction.handle_gesture(gesture_name, landmarks)
                else:
                    gesture_name = "Gesto non riconosciuto"
        else:
            gesture_name = "Nessun gesto riconosciuto"

        ############################################################################################

        # Disegna i landmarks sul frame e visualizza il nome del gesto
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Mostra il nome del gesto riconosciuto
        cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Mostra il frame
        cv2.imshow('Gesture Recognition', frame)

        # Mostra l'immagine caricata in una finestra separata
        if gesture_interaction.image is not None:
            cv2.imshow('Zoomed Image', gesture_interaction.image)  # Finestra separata per l'immagine


        # Esci dal ciclo se premi ESC
        if cv2.waitKey(1) & 0xFF == 27:  
            break

    # Rilascia la webcam e chiudi tutte le finestre
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
