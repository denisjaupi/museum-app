import cv2
import mediapipe as mp
import time

class ZoomingTest:
    def __init__(self):
        self.zoom_factor = 1.0        # Fattore di zoom iniziale
        self.max_zoom = 3.0           # Limite massimo di zoom
        self.min_zoom = 0.5           # Limite minimo di zoom
        self.min_distance = 30.0      # Distanza minima tra le dita per zoom out massimo
        self.max_distance = 200.0     # Distanza massima tra le dita per zoom in massimo
        self.zoom_sensitivity = 0.02  # Sensibilità del fattore di zoom
        self.stable_distance = None   # Distanza stabile da cui far partire lo zoom
        self.zooming_active = False   # Stato dello zoom (attivo/non attivo)
        self.previous_distance = None # Per memorizzare la distanza precedente

    def calculate_distance(self, point1, point2, frame_width, frame_height):
        """Calcola la distanza euclidea tra due punti, adattata alla dimensione del frame."""
        x1, y1 = int(point1.x * frame_width), int(point1.y * frame_height)
        x2, y2 = int(point2.x * frame_width), int(point2.y * frame_height)
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def normalize_zoom(self, current_dist):
        """Normalizza la distanza corrente tra le dita rispetto ai limiti minimi e massimi."""
        # Limita la distanza all'intervallo [min_distance, max_distance]
        normalized_dist = max(self.min_distance, min(current_dist, self.max_distance))
        # Mappa la distanza normalizzata sul range [min_zoom, max_zoom]
        zoom_range = self.max_zoom - self.min_zoom
        zoom_factor = (normalized_dist - self.min_distance) / (self.max_distance - self.min_distance)
        return self.min_zoom + zoom_factor * zoom_range

    def apply_zoom(self, image):
        """Applica il fattore di zoom all'immagine."""
        h, w = image.shape[:2]
        new_w = int(w * self.zoom_factor)
        new_h = int(h * self.zoom_factor)

        # Stampa le dimensioni originali e quelle ridimensionate
        print(f"[INFO] Original size: {w}x{h}, Zoom factor: {self.zoom_factor}, New size: {new_w}x{new_h}")

        # Ridimensiona l'immagine in base al fattore di zoom
        zoomed_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Taglia l'immagine se è più grande del frame originale
        if self.zoom_factor > 1.0:
            # Centra l'immagine tagliata
            crop_x = (new_w - w) // 2
            crop_y = (new_h - h) // 2
            zoomed_image = zoomed_image[crop_y:crop_y+h, crop_x:crop_x+w]
            print(f"[INFO] Zooming in, cropping to {w}x{h}, crop_x: {crop_x}, crop_y: {crop_y}")
        elif self.zoom_factor < 1.0:
            # TODO: Implementare il padding per lo zoom out
            # Se lo zoom factor è inferiore a 1.0, limitare al 100% dell'immagine
            zoomed_image = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
            print(f"[INFO] Zooming out, limited to original size {w}x{h}")
        
        return zoomed_image

    def process_zoom(self, current_distance):
        """Gestisce la logica del gesto di zoom in base alla distanza corrente tra le dita."""
        if self.stable_distance is None:
            # Imposta la stable_distance al min_distance o max_distance in base alla distanza iniziale
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
                # Logica per zoom in o zoom out
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
        self.stable_distance = None
        self.zooming_active = False
        self.previous_distance = None





def main():
    image = cv2.imread('IMG_4224.JPG')  # Carica l'immagine da zoomare

    if image is None:
        print("[ERROR] Immagine non trovata.")
        return

    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Inizializza la classe ZoomingTest
    zooming_test = ZoomingTest()

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

                # Disegna i landmarks e il vettore tra il pollice e l'indice
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = landmarks[4]
                index_finger_tip = landmarks[8]

                # Calcola la distanza tra pollice e indice
                currentDist = zooming_test.calculate_distance(thumb_tip, index_finger_tip, frame.shape[1], frame.shape[0])

                # Processa il gesto di zoom solo quando le dita raggiungono la distanza minima o massima
                zooming_test.process_zoom(currentDist)

                # Applica il fattore di zoom all'immagine
                zoomed_image = zooming_test.apply_zoom(image)

                # Mostra l'immagine zoomata
                cv2.imshow('Zoomed Image', zoomed_image)

        else:
            # Reset dello stato del gesto di zoom quando non ci sono mani
            zooming_test.reset_zoom()

        # Mostra il frame della webcam
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Esci premendo 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
