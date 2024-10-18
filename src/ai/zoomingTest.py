import cv2
import mediapipe as mp
import time

class ZoomingTest:
    def __init__(self):
        self.zoom_factor = 1.0  # Fattore di zoom iniziale
        self.max_zoom = 3.0     # Limite massimo di zoom
        self.min_zoom = 0.5     # Limite minimo di zoom
        self.last_zoom_time = 0  # Per evitare zoom troppo frequenti
        self.zoom_cooldown = 0.2  # Tempo di attesa tra un aggiornamento e l'altro (in secondi)
        self.motion_threshold = 10.0   # Soglia per determinare se le dita si stanno muovendo abbastanza
        self.zoom_speed_in = 0.1  # Velocità di zoom per ingrandire
        self.zoom_speed_out = 1.5  # Velocità di zoom per rimpicciolire (più veloce rispetto allo zoom in)
        self.last_stable_time = time.time()  # Tempo dell'ultimo aggiornamento di startDist
        self.stability_update_delay = 0.5  # Ritardo per aggiornare startDist (in secondi)

    def calculate_distance(self, point1, point2, frame_width, frame_height):
        """Calcola la distanza euclidea tra due punti, adattata alla dimensione del frame."""
        x1, y1 = int(point1.x * frame_width), int(point1.y * frame_height)
        x2, y2 = int(point2.x * frame_width), int(point2.y * frame_height)
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

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
            # Se il fattore di zoom è minore di 1, aggiungi bordi neri
            border_x = (w - new_w) // 2
            border_y = (h - new_h) // 2
            zoomed_image = cv2.copyMakeBorder(zoomed_image, border_y, border_y, border_x, border_x, cv2.BORDER_CONSTANT)
            print(f"[INFO] Zooming out, adding borders {border_x}px horizontally, {border_y}px vertically")
        
        return zoomed_image


def main():
    startDist = None  # La distanza iniziale tra il pollice e l'indice
    previousDist = None  # La distanza tra le dita nel frame precedente
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

        # Imposta il tempo corrente all'inizio del ciclo
        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark

                # Disegna i landmarks e il vettore tra il pollice e l'indice
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = landmarks[4]
                index_finger_tip = landmarks[8]
                thumb_coords = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))
                index_coords = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))

                # Calcola la distanza tra pollice e indice
                currentDist = zooming_test.calculate_distance(thumb_tip, index_finger_tip, frame.shape[1], frame.shape[0])

                # Aggiorna la distanza iniziale quando le dita sono stabili
                if startDist is None:
                    startDist = currentDist  # Imposta la distanza iniziale

                # Differenza di distanza per calcolare lo zoom
                if previousDist is None:
                    previousDist = currentDist  # Imposta la distanza precedente al valore attuale

                distance_change = currentDist - startDist
                distance_variation = abs(currentDist - previousDist)  # Variazione rispetto al frame precedente

                # Stampa la distanza tra le dita e il cambiamento
                print(f"[INFO] Current distance: {currentDist}, Start distance: {startDist}, Distance change: {distance_change}, Variation from previous: {distance_variation}")

                # Se la variazione tra la distanza corrente e quella precedente è superiore alla soglia di movimento
                if distance_variation > zooming_test.motion_threshold:
                    # Controlla il cooldown del zoom
                    if current_time - zooming_test.last_zoom_time > zooming_test.zoom_cooldown:
                        # Differenzia la velocità di zoom per zoom in/out
                        if distance_change > 0:
                            zooming_test.zoom_factor += (distance_change / startDist) * zooming_test.zoom_speed_in
                        elif distance_change < 0:
                            zooming_test.zoom_factor += (distance_change / startDist) * zooming_test.zoom_speed_out

                        # Limita il fattore di zoom
                        zooming_test.zoom_factor = max(zooming_test.min_zoom, min(zooming_test.zoom_factor, zooming_test.max_zoom))

                        # Stampa il nuovo fattore di zoom
                        print(f"[INFO] Zoom factor updated: {zooming_test.zoom_factor}")

                        # Aggiorna il tempo dell'ultimo zoom
                        zooming_test.last_zoom_time = current_time
                else:
                    # Se le dita sono ferme, aggiorna il valore di startDist solo se il tempo è trascorso
                    if current_time - zooming_test.last_stable_time > zooming_test.stability_update_delay:
                        startDist = currentDist
                        zooming_test.last_stable_time = current_time  # Aggiorna il tempo dell'ultimo aggiornamento
                        print(f"[INFO] Fingers stable, updating start distance: {startDist}")

                # Applica il fattore di zoom all'immagine
                zoomed_image = zooming_test.apply_zoom(image)

                # Mostra l'immagine zoomata
                cv2.imshow('Zoomed Image', zoomed_image)

                # Disegna la linea tra pollice e indice
                cv2.line(frame, thumb_coords, index_coords, (0, 255, 0), 2)

                # Aggiorna la distanza precedente
                previousDist = currentDist

        else:
            # Reset della distanza iniziale se non ci sono mani rilevate
            startDist = None
            previousDist = None

        # Mostra il frame della webcam
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Esci premendo 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
