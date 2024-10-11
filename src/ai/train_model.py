import os
import pandas as pd
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer
import matplotlib.pyplot as plt

assert tf.__version__.startswith('2')

class GestureModelTrainer:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.dataset = None
        self.model = None

    def load_data(self):
        """Carica i dati dai file CSV presenti nella cartella data_dir e usa il nome del file come label."""
        dataframes = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    # Carica il DataFrame
                    df = pd.read_csv(filepath, on_bad_lines='skip')
                    
                    # Estrai il nome del file senza estensione e aggiungilo come colonna 'label'
                    label = os.path.splitext(filename)[0]  # Ottieni il nome del file senza estensione
                    df['label'] = label  # Aggiungi la colonna 'label' al DataFrame

                    dataframes.append(df)
                    print(f"File {filename} caricato con successo.")
                except Exception as e:
                    print(f"Errore durante la lettura del file {filename}: {e}")

        if not dataframes:
            print("Nessun DataFrame è stato caricato. Controlla i tuoi file CSV.")
            return None  # Restituisci None se non ci sono DataFrame

        # Concatenare tutti i DataFrame in uno solo
        self.dataset = pd.concat(dataframes, ignore_index=True)
        print(f"Dati caricati: {self.dataset.shape[0]} righe e {self.dataset.shape[1]} colonne.")
        return self.dataset

    def train_model(self):
        """Addestra il modello di riconoscimento gesti."""
        if self.dataset is None:
            raise ValueError("I dati devono essere caricati prima di addestrare il modello.")
        
        # Stampa le colonne del dataset
        print("Colonne nel dataset:", self.dataset.columns.tolist())

        # Assicurati che la colonna 'label' esista
        if 'label' not in self.dataset.columns:
            raise KeyError("'label' non trovato nel dataset. Assicurati che la colonna esista.")

        # Preparare i dati
        X = self.dataset.drop('label', axis=1)
        y = self.dataset['label']

        # Suddividere il dataset in set di addestramento e di test
        train_size = int(0.8 * len(X))
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Creare e addestrare il modello
        self.model = gesture_recognizer.create_model(X_train, y_train)
        history = self.model.fit(X_train, y_train, epochs=50, validation_split=0.2)
        print("Modello addestrato.")
        return history  # Restituisci la storia per la tracciatura

    def evaluate_model(self):
        """Valuta le prestazioni del modello."""
        if self.model is None:
            raise ValueError("Il modello deve essere addestrato prima di valutarlo.")
        
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test)
        print(f"Perdita del test: {test_loss}, Accuratezza del test: {test_accuracy}")

    def plot_training_history(self, history):
        """Traccia la storia di addestramento."""
        plt.plot(history.history['accuracy'], label='Accuratezza di addestramento')
        plt.plot(history.history['val_accuracy'], label='Accuratezza di validazione')
        plt.xlabel('Epoch')
        plt.ylabel('Accuratezza')
        plt.legend()
        plt.title('Accuratezza del Modello')
        plt.show()


if __name__ == "__main__":
    # Specifica la directory contenente i file CSV
    data_directory = 'src/ai/dataset' 
    trainer = GestureModelTrainer(data_directory)
    
    # Carica i dati, addestra il modello e valuta le prestazioni
    dataset = trainer.load_data()
    history = trainer.train_model()
    trainer.evaluate_model()
    trainer.plot_training_history(history)
