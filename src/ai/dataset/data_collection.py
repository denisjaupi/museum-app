import cv2
import mediapipe as mp
import csv
import os

##########################################

gesture_classes = {
    0: "Index up",
    1: "Index middle up",
    2: "Zoom in \ Zoom out"
}

##########################################

# MediaPipe hands initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Directory to save collected data
data_dir = os.path.join('src', 'ai', 'dataset')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Set the name of the CSV file where data will be saved
csv_file_path = os.path.join(data_dir, 'gestures_data.csv')

# Function to save landmark data to CSV
def save_landmarks_to_csv(landmarks, gesture_class):
    with open(csv_file_path, mode='a', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        row = [gesture_class] + [coord for landmark in landmarks for coord in (landmark.x, landmark.y, landmark.z)]
        csv_writer.writerow(row)

# Print available gestures
print("Seleziona il gesto da raccogliere:")
for key, value in gesture_classes.items():
    print(f"{key}: {value}")

# Input for gesture classification
gesture_class = int(input("Inserisci il numero della classe del gesto: "))

print(f"Inizia la raccolta dati per: {gesture_classes[gesture_class]}")
print("Premi 'q' per uscire.")

# Video capture from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Errore nel rilevamento dell'immagine dalla webcam.")
        break

    # Convert BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and get the hand landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Save the landmarks (21 points for each hand)
            save_landmarks_to_csv(hand_landmarks.landmark, gesture_class)
            
            # Draw the hand landmarks on the image for visualization
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Show the image with hand landmarks
    cv2.imshow('Raccolta Dati Gesti', image)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

print(f"I dati dei gesti sono stati salvati nel file: {csv_file_path}")
