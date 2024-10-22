import pyautogui
import cv2
import mediapipe as mp
import time
import collections

class IndexMiddleUpController:
    
    def __init__(self):
        self.smoothing_factor = 5  # Fattore di smussatura
        self.last_position = None
        self.last_move_time = time.time()
        self.screen_width, self.screen_height = pyautogui.size()
        # Coda per memorizzare le ultime 5 posizioni del dito
        self.pointer_positions = collections.deque(maxlen=self.smoothing_factor)

    def smooth(self, new_position):
        self.pointer_positions.append(new_position)
        avg_x = sum(pos[0] for pos in self.pointer_positions) / len(self.pointer_positions)
        avg_y = sum(pos[1] for pos in self.pointer_positions) / len(self.pointer_positions)
        return int(avg_x), int(avg_y)


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
        
    def execute(self, landmarks):
        index_finger_tip = landmarks[8]  # Punta dell'indice
        self.scroll(index_finger_tip)



def main():
    # Inizializza MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    # Inizializza la classe IndexUpController
    index_up_controller = IndexMiddleUpController()

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

