import cv2
import mediapipe as mp


class ZoomingController:
    
    def __init__(self):
        self.zoom_factor = 1.0        # Fattore di zoom iniziale
        self.max_zoom = 3.0           # Limite massimo di zoom
        self.min_zoom = 1.0           # Limite minimo di zoom
        self.min_distance = 30.0      # Distanza minima tra le dita per zoom out massimo
        self.max_distance = 200.0     # Distanza massima tra le dita per zoom in massimo
        self.initial_distance = None   # Distanza iniziale tra le dita
        self.stable_distance = None    # Distanza stabile da cui far partire lo zoom
        self.zooming_active = False     # Stato dello zoom (attivo/non attivo)
        self.previous_distance = None    # Per memorizzare la distanza precedente

    def calculate_distance(self, point1, point2, frame_width, frame_height):
        """Calcola la distanza euclidea tra due punti, adattata alla dimensione del frame."""
        x1, y1 = int(point1.x * frame_width), int(point1.y * frame_height)
        x2, y2 = int(point2.x * frame_width), int(point2.y * frame_height)
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def normalize_zoom(self, current_dist):
        """Normalizza la distanza corrente tra le dita rispetto ai limiti minimi e massimi."""
        normalized_dist = max(self.min_distance, min(current_dist, self.max_distance))
        zoom_range = self.max_zoom - self.min_zoom
        zoom_factor = (normalized_dist - self.min_distance) / (self.max_distance - self.min_distance)
        return self.min_zoom + zoom_factor * zoom_range

    def apply_zoom(self, image):
        """Applica il fattore di zoom all'immagine centrando lo zoom sull'immagine stessa."""
        h, w = image.shape[:2]
        new_w, new_h = int(w * self.zoom_factor), int(h * self.zoom_factor)

        # Calcola il ridimensionamento dell'immagine
        zoomed_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Calcola il punto di partenza per il cropping basato sull'offset
        start_x = max((new_w // 2) - (w // 2), 0)
        start_y = max((new_h // 2) - (h // 2), 0)

        # Croppa l'immagine zoomata
        zoomed_image = zoomed_image[start_y:start_y + h, start_x:start_x + w]

        return zoomed_image

    def process_zoom(self, current_distance):
        """Gestisce la logica del gesto di zoom in base alla distanza corrente tra le dita."""
        if self.stable_distance is None:
            if current_distance <= self.min_distance:
                self.stable_distance = self.min_distance
                self.zooming_active = True
                print(f"[INFO] Zoom out gesture detected, stable distance set to {self.stable_distance}")
            elif current_distance >= self.max_distance:
                self.stable_distance = self.max_distance
                self.zooming_active = True
                print(f"[INFO] Zoom in gesture detected, stable distance set to {self.stable_distance}")

        # Se lo zoom è attivo
        if self.zooming_active:
            if self.previous_distance is not None:
                if self.stable_distance == self.max_distance and current_distance < self.previous_distance:
                    # Zoom out quando la distanza diminuisce
                    normalized_zoom = self.normalize_zoom(current_distance)
                    self.zoom_factor = normalized_zoom
                    print(f"[INFO] Zoom out")
                elif self.stable_distance == self.min_distance and current_distance > self.previous_distance:
                    # Zoom in quando la distanza aumenta
                    normalized_zoom = self.normalize_zoom(current_distance)
                    self.zoom_factor = normalized_zoom
                    print(f"[INFO] Zoom in")

        # Memorizza la distanza corrente per il confronto successivo
        self.previous_distance = current_distance

    def reset_zoom(self):
        """Resetta lo stato dello zoom gesture."""
        print("[INFO] Zoom gesture reset")
        self.initial_distance = None  # Reset della distanza iniziale
        self.stable_distance = None
        self.zooming_active = False
        self.previous_distance = None

    def execute(self, landmarks, image):
        print("[DEBUG] ZoomingController.execute chiamato")
        """Esegue il controllo del gesto di zoom usando i landmarks 4 e 8."""
        thumb_tip = landmarks[4]  # Punta del pollice
        index_finger_tip = landmarks[8]  # Punta dell'indice

        # Calcola la distanza tra pollice e indice
        current_distance = self.calculate_distance(thumb_tip, index_finger_tip, image.shape[1], image.shape[0])

        # Processa il gesto di zoom
        self.process_zoom(current_distance)

        # Applica lo zoom all'immagine
        zoomed_image = self.apply_zoom(image)

        return zoomed_image  # Restituisce l'immagine zoomata



def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    # Inizializza la classe ZoomingController
    zooming_controller = ZoomingController()

    # Carica l'immagine da zoomare
    image_path = 'IMG_Test.JPG'
    image = cv2.imread(image_path)

    if image is None:
        print("[ERROR] Immagine non trovata.")
        return

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

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark

                # Disegna i landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Esegui il controllo del gesto di zoom
                zoomed_image = zooming_controller.execute(landmarks, image)

                # Mostra l'immagine zoomata
                cv2.imshow('Zoomed Image', zoomed_image)

        else:
            # Reset dello stato del gesto di zoom quando non ci sono mani rilevate
            zooming_controller.reset_zoom()

        # Mostra il frame della webcam
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Esci premendo 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
