import time
import pyautogui
import cv2
import mediapipe as mp
import collections

class IndexUpController:
    def __init__(self):
        self.smoothing_factor = 5  # Fattore di smussatura
        self.last_position = None
        self.last_move_time = time.time()
        self.screen_width, self.screen_height = pyautogui.size()
        # Coda per memorizzare le ultime 5 posizioni del dito
        self.pointer_positions = collections.deque(maxlen=self.smoothing_factor)
        self.click_blocked = False
        self.last_click_time = 0

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
                # Se il mouse è fermo per più di 2.5 secondi, esegui il click
                if current_time - self.last_move_time > 2.5:
                    pyautogui.click() 
                    print("Click eseguito!")
                    self.click_blocked = True  # Blocca ulteriori click
                    self.last_click_time = current_time  # Aggiorna l'ultimo click eseguito
            else:
                # Se il mouse si è mosso, aggiorna il timer
                self.last_move_time = current_time

        # Aggiorna l'ultima posizione del mouse
        self.last_position = (mouse_x, mouse_y)

    def execute(self, landmarks):
        index_finger_tip = landmarks[8]  # Punta dell'indice
        self.move_mouse(index_finger_tip)
        self.click(index_finger_tip)

def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    # Inizializza la classe IndexUpController
    index_up_controller = IndexUpController()

    # Inizializza la webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Non è stato possibile acquisire il frame dalla webcam.")
            break

        # Ribalta il frame orizzontalmente per evitare l'effetto specchiato
        frame = cv2.flip(frame, 1)

        # Converti il frame in RGB per MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark

                # Disegna i landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Esegui il controllo del gesto
                index_up_controller.execute(landmarks)

        # Mostra il frame della webcam
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Esci premendo 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
