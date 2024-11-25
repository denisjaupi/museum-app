#################--------MAIN--------#################

# Controllo frame rate
FRAME_RATE = 30  # Frame per second

# Interruttore AI
ENABLE_AI = False  



#################--------DATABASE--------#################

# Configurazione database
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "museum_app_db",
    "user": "postgres",
    "password": "postgres"
}



#################--------GESTURES--------#################

### Per aggiungere i gesti (data_collection.py): ###

# 1 - Aggiungere il nome del gesto e il numero di classe corrispondente
#     alla mappa dei gesti (gesture_classes).

# 2 - Avviare il file data_collection.py.

# 3 - Dopo aver scritto sul terminale il numero corrispondente al nuovo gesto,
#     fare il gesto davanti alla webcam per registrarli.

# 4 - Premere 'q' per terminare la registrazione.

# 5 - I nuovi gesti saranno salvati in gestures_data.csv.

# 6 - Avviare il file train_model.py per addestrare il modello.

# 7 - Una volta addestrato il modello avviare gesture_recognition.py per debug.

# 8 - Aggiungere una classe per la logica del nuovo gesto in ai/utils.

# 9 - Una volta scritta la classe (con i giusti import) avviare gesture_interaction.py per debug.

# 10 - Avviare il main.py per testare il nuovo gesto (ENABLE_AI = True).





