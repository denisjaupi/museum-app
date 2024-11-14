import cv2
import mediapipe as mp
import gesture_recognition as gr
from utils import zooming_gesture as zg
from utils import indexUp_gesture as ig
from utils import indexMiddleUp_gesture as img


class GestureInteraction:

    def __init__(self):
        self.image = None  # L'immagine per lo zoom
        self.zoomed_image = None  # Immagine zoomata

        self.index_up_controller = ig.IndexUpController()
        self.index_middle_up_controller = img.IndexMiddleUpController()
        self.zooming_controller = zg.ZoomingController()


    def set_image(self, image_path):
        """Carica un'immagine da un percorso specificato."""
        self.image = cv2.imread(image_path)
        if self.image is None:
            print(f"[ERROR] Impossibile caricare l'immagine da {image_path}. Verifica il percorso.")
        else:
            print(f"[INFO] Immagine caricata con successo da {image_path}.")


    def get_zoomed_image(self):
        return self.zoomed_image if self.zoomed_image is not None else self.image


    def handle_gesture(self, gesture_name, landmarks):
        if gesture_name == "Index up" or gesture_name == "Index still up":
            print("[INFO] Esecuzione 'Index Up'")
            self.index_up_controller.execute(landmarks)
        elif gesture_name == "Index middle up":
            print("[INFO] Esecuzione 'Index Middle Up'")
            self.index_middle_up_controller.execute(landmarks)
        elif gesture_name == "Zoom in / Zoom out":
            print("[INFO] Esecuzione 'Zoom In/Out'")
            self.zoomed_image = self.zooming_controller.execute(landmarks, self.image)
        else:
            print("[WARNING] Gesto non riconosciuto.")



def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)

    # Inizializza il riconoscimento dei gesti e l'interazione
    gesture_detector = gr.GestureModelDetector() 
    gesture_interaction = GestureInteraction()

    # Carica un'immagine da visualizzare e zoomare (schermo intero)
    image_path = 'src/app/images/operas/cappella_magi_est.jpg'  
    gesture_interaction.set_image(image_path)

    # Imposta la finestra di visualizzazione per l'immagine zoomata
    cv2.namedWindow("Zoomed Image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Zoomed Image", gesture_interaction.zooming_controller.set_mouse_position)

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

            # Prevedi il gesto usando il modello addestrato
            gesture_id = gesture_detector.predict_gesture(landmarks)
            gesture_name = gesture_detector.class_labels[gesture_id]

            # Verifica i gesti riconosciuti dal modello e gestisci le azioni
            if gesture_name == "Index up" or\
                 gesture_name == "Index middle up" or\
                     gesture_name == "Zoom in / Zoom out":
                gesture_interaction.handle_gesture(gesture_name, landmarks)

                # Mostra l'immagine zoomata solo se c'è stato uno zoom
                zoomed_image = gesture_interaction.get_zoomed_image()
                if zoomed_image is not None:
                    cv2.imshow('Zoomed Image', zoomed_image)

            else:
                # Se non viene riconosciuto nessuno degli altri gesti, 
                # controlla se l'indice è alzato per il movimento del mouse
                if gesture_detector.is_index_finger_up(landmarks): 
                    gesture_name = "Index still up"
                    gesture_interaction.handle_gesture(gesture_name, landmarks)
                else:
                    gesture_name = "Gesture not recognized"
            
        else:
            gesture_name = "Hand not detected"
            gesture_interaction.zooming_controller.reset_zoom()

        # Disegna i landmarks sul frame e visualizza il nome del gesto
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Mostra il nome del gesto riconosciuto
        cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Mostra il frame
        cv2.imshow('Gesture Recognition', frame)

        # Esci dal ciclo se premi ESC
        if cv2.waitKey(1) & 0xFF == 27:  
            break

    # Rilascia la webcam e chiudi tutte le finestre
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
