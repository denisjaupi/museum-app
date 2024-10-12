import os
import pandas as pd
from sklearn.model_selection import train_test_split
import mediapipe_model_maker as mm


class GestureModelTrainer:

    def __init__(self, data_dir):
        self.data_dir = data_dir  # Directory contenente i file CSV
        self.dataset = None  # Dataset completo verrà memorizzato qui

    def load_data(self):
        """
        Carica i dati dai file CSV presenti nella cartella data_dir.
        Aggiunge il nome del file come etichetta (label) per ogni file CSV.
        """
        dataframes = []  # Lista per memorizzare i DataFrame caricati

        # Passo 1: Iterare su tutti i file nella cartella data_dir
        for filename in os.listdir(self.data_dir):
            # Passo 2: Creare il percorso completo per il file CSV
            filepath = os.path.join(self.data_dir, filename)
            
            try:
                # Passo 3: Caricare il file CSV in un DataFrame, saltando righe malformate
                df = pd.read_csv(filepath, on_bad_lines='skip')
                
                # Controlla se il DataFrame ha 63 colonne (21 landmarks con 3 coordinate ciascuno)
                if df.shape[1] != 63:
                    print(f"Attenzione: il file {filename} non ha il formato corretto (dovrebbe avere 63 colonne).")
                    continue  # Salta il file se non è formattato correttamente

                # Passo 4: Utilizzare il nome del file (senza estensione) come etichetta
                label = os.path.splitext(filename)[0]  # Nome del file senza estensione
                df['label'] = label  # Aggiungi la colonna 'label' al DataFrame

                # Passo 5: Aggiungere il DataFrame alla lista dei DataFrame
                dataframes.append(df)
                print(f"File {filename} caricato con successo.")
            
            except Exception as e:
                # Passo 6: Gestire eventuali errori di caricamento
                print(f"Errore durante la lettura del file {filename}: {e}")

        # Passo 7: Concatenare tutti i DataFrame in un unico dataset
        if dataframes:
            self.dataset = pd.concat(dataframes, ignore_index=True).drop_duplicates()  # Rimuove eventuali duplicati
            print(f"Dati caricati: {self.dataset.shape[0]} righe e {self.dataset.shape[1]} colonne.")
        else:
            print("Nessun dato caricato.")
        
        # Passo 8: Restituire il dataset completo
        return self.dataset
    
    def prepare_data(self):
        """Prepara i dati per l'addestramento, validazione e test."""
        if self.dataset is None:
            raise ValueError("I dati devono essere caricati prima di prepararli.")

        # Separare le features e le etichette
        X = self.dataset.drop('label', axis=1)
        y = self.dataset['label']

        # Suddividere il dataset in addestramento e test (80% / 20%)
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        # Suddividere il dataset temporaneo in validazione e test (50% / 50% del set temporaneo)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

        # Creare DataFrame per i dati di addestramento, validazione e test
        train_df = pd.DataFrame(X_train)
        train_df['label'] = y_train.reset_index(drop=True)

        val_df = pd.DataFrame(X_val)
        val_df['label'] = y_val.reset_index(drop=True)

        test_df = pd.DataFrame(X_test)
        test_df['label'] = y_test.reset_index(drop=True)

        return train_df, val_df, test_df

    def train_model(self, train_df, val_df):

        """Definisce i parametri per il modello, crea e addestra il modello."""

        # Crea un dataset in base alla documentazione della libreria
        train_data = mm.gesture_recognizer.Dataset(train_df.drop('label', axis=1).values, train_df['label'].values)
        val_data = mm.gesture_recognizer.Dataset(val_df.drop('label', axis=1).values, val_df['label'].values)
        options=mm.gesture_recognizer.GestureRecognizerOptions()

        # Creare il modello di riconoscimento gesti
        model = mm.gesture_recognizer.GestureRecognizer.create(
            train_data=train_data,
            validation_data=val_data,
            options=options
            #batch_size=model_params['batch_size'],
            #epochs=model_params['epochs'],
            #learning_rate=model_params['learning_rate']
        )

        # Definire il numero di epoche e dimensione del batch qui
        epochs = 50
        batch_size = 32

        # Addestrare il modello
        history = model.fit(
            train_data=train_data,
            validation_data=val_data,
            epochs=epochs,
            batch_size=batch_size
        )

        print("Modello addestrato con successo.")
        return model, history
        
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
    train_df, val_df, test_df = trainer.prepare_data()

    # Addestrare il modello
    model, history = trainer.train_model(train_df, val_df)

    # Mostrare le forme dei DataFrame
    print("Forma del train set:", train_df.shape)
    print("Forma del validation set:", val_df.shape)
    print("Forma del test set:", test_df.shape)

