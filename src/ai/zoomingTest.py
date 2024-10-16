import cv2
import mediapipe as mp
import time

class ZoomingTest:
    def __init__(self):
        self.last_zoom_time = 0
        self.zoom_state = None
        self.initial_distance = None  # Distanza iniziale tra le dita
        self.scale_factor = 1.0  # Fattore di scala per lo zoom
        self.max_zoom = 3.0  # Zoom massimo
        self.min_zoom = 0.5  # Zoom minimo

    def calculate_distance(self, point1, point2):
        """Calcola la distanza euclidea tra due punti."""
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    def zoom_in(self, distance):
        """Esegui lo zoom in basato sulla distanza."""
        self.scale_factor *= distance
        self.scale_factor = min(self.scale_factor, self.max_zoom)
        print(f"Zoom in - Fattore di scala: {self.scale_factor}")

    def zoom_out(self, distance):
        """Esegui lo zoom out basato sulla distanza."""
        self.scale_factor /= distance
        self.scale_factor = max(self.scale_factor, self.min_zoom)
        print(f"Zoom out - Fattore di scala: {self.scale_factor}")

    def apply_zoom(self, image):
        """Applica lo zoom all'immagine in base al fattore di scala."""
        height, width = image.shape[:2]
        new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
        zoomed_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

        # Se l'immagine è più grande dello schermo, centrarla
        if new_size[0] > width or new_size[1] > height:
            offset_x = (new_size[0] - width) // 2
            offset_y = (new_size[1] - height) // 2
            zoomed_image = zoomed_image[offset_y:offset_y+height, offset_x:offset_x+width]

        return zoomed_image

    def handle_zoom(self, landmarks):
        """Gestisce il gesto di zoom in base alla distanza relativa tra due landmarks."""
        thumb_tip = landmarks[4]
        index_finger_tip = landmarks[8]
        distance = self.calculate_distance(thumb_tip, index_finger_tip)

        # Se non abbiamo una distanza iniziale, la memorizziamo
        if self.initial_distance is None:
            self.initial_distance = distance
            return  # Non facciamo nulla finché non abbiamo una distanza iniziale

        # Calcola il fattore di scala in base alla distanza attuale e quella iniziale
        scale_factor = distance / self.initial_distance

        # Blocca le oscillazioni rilevando solo cambiamenti significativi nel fattore di scala
        if abs(scale_factor - 1) < 0.05:
            return  # Ignora piccoli cambiamenti

        current_time = time.time()

        # Inizio dello zoom in o out in base al movimento delle dita
        if scale_factor > 1:
            self.zoom_in(scale_factor)
        else:
            self.zoom_out(scale_factor)

        # Aggiorna lo stato dell'ultimo zoom
        self.last_zoom_time = current_time

def main():
    # Carica l'immagine da zoomare
    image = cv2.imread('IMG_4224.JPG')
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

                # Gestisci il gesto di zoom
                zooming_test.handle_zoom(landmarks)

                # Disegna i landmarks e il vettore tra il pollice e l'indice
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = landmarks[4]
                index_finger_tip = landmarks[8]
                thumb_coords = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))
                index_coords = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))
                cv2.line(frame, thumb_coords, index_coords, (0, 255, 0), 2)

        # Applica lo zoom all'immagine
        zoomed_image = zooming_test.apply_zoom(image)

        # Mostra il frame della webcam e l'immagine zoomata
        cv2.imshow('Zooming Test', frame)
        cv2.imshow('Zoomed Image', zoomed_image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
