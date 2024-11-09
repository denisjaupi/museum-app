import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class GestureModelTrainer:

    def __init__(self, data_dir):
        self.data_dir = data_dir  # Directory contenente il file CSV
        self.dataset = None  # Dataset completo verrà memorizzato qui

    def load_data(self):
        """Carica i dati dal file CSV."""


        data_path = self.data_dir
        self.dataset = pd.read_csv(data_path, header=None, on_bad_lines="skip")
        self.dataset.columns = ['label'] + [f'coord_{i}' for i in range(1, len(self.dataset.columns))]
        print(f"[INFO] Dati caricati con successo! Numero di campioni: {len(self.dataset)}")

    def prepare_data(self):
        """Prepara i dati per l'addestramento, validazione e test."""


        print("[INFO] Preparazione dei dati: suddivisione in train, val, test...")
        
        # Mescola i dati
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)

        # Dividi le caratteristiche dalle etichette
        X = self.dataset.drop(columns=['label'])
        y = self.dataset['label']

        # Suddivisione train, val, test
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        print(f"[INFO] Dati preparati!")
        print(f" - Campioni di training: {len(X_train)}")
        print(f" - Campioni di validazione: {len(X_val)}")
        print(f" - Campioni di test: {len(X_test)}")

        return X_train, X_val, X_test, y_train, y_val, y_test

    def train_model(self, train_df, val_df, test_df):
        """Allena un modello e valuta le sue prestazioni."""


        print("[INFO] Inizio dell'addestramento del modello...")

        model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Addestramento
        model.fit(train_df[0], train_df[1])
        print("[INFO] Addestramento completato!")

        # Validazione
        val_predictions = model.predict(val_df[0])
        val_accuracy = accuracy_score(val_df[1], val_predictions)
        print(f'Validation Accuracy: {val_accuracy}')
        print(f"[INFO] Accuratezza sul set di validazione: {val_accuracy:.4f}")

        # Test finale
        test_predictions = model.predict(test_df[0])
        test_accuracy = accuracy_score(test_df[1], test_predictions)
        print(f'Test Accuracy: {test_accuracy}')
        print(f"[INFO] Accuratezza sul set di test: {test_accuracy:.4f}")

        return model
    
    def save_model(self, model, model_path='gesture_recognition_model.pkl'):
        """ Salva il modello addestrato in un file .pkl per poterlo riutilizzare successivamente. """


        print(f"[INFO] Salvataggio del modello in {model_path}...")

        try:
            joblib.dump(model, model_path)
            print(f"[INFO] Modello salvato con successo in {model_path}!")
        except Exception as e:
            print(f"[ERROR] Errore durante il salvataggio del modello: {str(e)}")



if __name__ == "__main__":
    
    # Definisci la directory dove si trova il file CSV
    data_dir = 'src/ai/dataset/gestures_data.csv'  

    # Istanzia l'oggetto GestureModelTrainer
    trainer = GestureModelTrainer(data_dir)

    # 1. Carica i dati
    print("Caricamento dei dati...")
    trainer.load_data()
    print("Dati caricati con successo!")

    # 2. Prepara i dati per addestramento, validazione e test
    print("Preparazione dei dati per l'addestramento...")
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.prepare_data()
    print("Dati preparati!")

    # 3. Addestramento del modello
    print("Inizio dell'addestramento del modello...")
    model = trainer.train_model((X_train, y_train), (X_val, y_val), (X_test, y_test))
    print("Modello addestrato con successo!")

    # 4. Salva il modello addestrato per usi futuri
    model_path='src/ai/model/gesture_recognition_model.pkl'
    print("[INFO] Salvataggio del modello in gesture_recognition_model.pkl...")
    trainer.save_model(model, model_path)
    print("[INFO] Modello salvato con successo in gesture_recognition_model.pkl!")


    print("Processo completato!")

    