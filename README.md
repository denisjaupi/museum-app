# Sistema di interazione uomo-macchina basato su riconoscimento gestuale con applicazione ai beni culturali

In questo progetto è stato sviluppato un sistema di interazione uomo-macchina basato sul riconoscimento gestuale utilizzando framework quali MediaPipe e OpenCV. 
La rilevazione dei gesti manuali è stata conseguita attraverso l'addestramento di una rete neurale implementata con il modello Random Forest, sviluppato tramite scikit-learn. 
Il processo di apprendimento si è basato su un dataset composto da file CSV contenenti le coordinate dei landmark digitali, consentendo un'analisi dettagliata e precisa dei movimenti gestuali.
Il sistema è stato applicato su una GUI sviluppata con Kivy, appositamente progettata per l'analisi interattiva e dettagliata delle opere d'arte.

## Indice
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Struttura del Progetto](#struttura-del-progetto)
- [Moduli](#moduli)
- [Licenza](#licenza)

## Installazione

### 1. Assicurati che Python 3.11 sia Installato

Il progetto è stato sviluppato e testato con Python 3.11. Per verificare la versione di Python installata:

```sh
python --version
```

Se è necessario installare Python 3.11, puoi scaricarlo dal sito ufficiale:  
[Download Python 3.11](https://www.python.org/downloads/)

Oppure, puoi utilizzare un gestore di pacchetti (su macOS o Linux):

```sh
# Su macOS con Homebrew:
brew install python@3.11

# Su Linux con APT (Ubuntu/Debian):
sudo apt update
sudo apt install python3.11
```

### 2. Clonare il Repository

Clona il repository del progetto sulla tua macchina locale:

```sh
git clone https://github.com/denisjaupi/museum-app
cd museum-app
```

### 3. Creare e Attivare un Ambiente Virtuale con Python 3.11

Crea un ambiente virtuale utilizzando Python 3.11:

```sh
python3.11 -m venv venv
```

Attiva l'ambiente virtuale:

- Su macOS/Linux:
    ```sh
    source venv/bin/activate
    ```

- Su Windows:
    ```sh
    .\venv\Scripts\activate
    ```

### 4. Installare le Dipendenze

Installa le dipendenze elencate nel file `requirements.txt`. Utilizza il risolutore legacy per evitare eventuali problemi con l'installazione dei pacchetti:

```sh
pip install -r requirements.txt --use-deprecated=legacy-resolver
```

### 5. Assicurati che PostgreSQL 16.2 sia Installato

Il progetto utilizza PostgreSQL 16.2 per la gestione del database. Per verificare se PostgreSQL è installato:

```sh
psql --version
```

Se PostgreSQL non è installato o se desideri installare una versione specifica (ad esempio la 16.2), puoi farlo utilizzando i seguenti metodi:

- **macOS (Homebrew):**
    ```sh
    brew install postgresql@16
    ```

- **Ubuntu/Debian:**
    ```sh
    sudo apt update
    sudo apt install postgresql-16
    ```

- **Windows:**
    Scarica e installa PostgreSQL 16.2 dal sito ufficiale:  
    [Download PostgreSQL](https://www.postgresql.org/download/)

### 6. Configurare il Database PostgreSQL

Puoi configurare il database utilizzando pgAdmin4 o direttamente tramite terminale. Ecco i passaggi per configurarlo tramite pgAdmin4:

1. Apri pgAdmin4.
2. Connettiti alla tua istanza di PostgreSQL.
3. Crea un nuovo database (ad esempio `museum_app_db`).

### 7. Ripristinare il Database dal File `db_dump.sql`

Naviga nella directory `src/app/database` e ripristina il database utilizzando il file `db_dump.sql`:

```sh
cd src/app/database
psql -h <host> -p 5432 -U <username> -d <dbname> -f db_dump.sql
```

Sostituisci `<host>`, `<username>`, e `<dbname>` con i dettagli di connessione del tuo database PostgreSQL.

### 8. Aggiornare le Credenziali del Database nel File `config.py`

Nel file `config.py`, aggiorna la sezione `DB_CONFIG` con le credenziali del tuo database PostgreSQL (host, utente, password e nome del database):

```python
DB_CONFIG = {
    'host': '<tuo_host>',
    'user': '<tuo_utente>',
    'password': '<tua_password>',
    'dbname': '<tuo_dbname>'
}
```

## Utilizzo

1. Modifica i parametri del file `config.py` se necessario
   
2. Esegui lo script principale:
    ```sh
    python main.py
    ```

## Struttura del Progetto

```plaintext
museum_app/
└── src/
    └── ai/
        └── dataset/
            └── data_collection.py
            └── gestures_data.csv
        └── model/
            └── gesture_recognition_model.pkl
            └── train_model.py
        └── utils/
            └── indexMiddleUp_gesture.py
            └── indexUp_gesture.py
            └── zooming_gesture.py
        └── gesture_interaction.py
        └── gesture_recognition.py
    └── app/
        └── database/
            └── db_connection.py
            └── db_dump.sql
            └── db_instance.py
        └── images/
        └── utils/
        └── views/
    └── config.py
    └── main.py
└── requirements.txt/

```

## Moduli

### `main.py`
Lo script principale che gestisce il caricamento, il processamento e la visualizzazione dei dati.

### `config.py`
Contiene parametri di configurazione del progetto.

### `app/database/db_dump.sql`
Contiene la copia del database da scaricare per far funzionare al meglio la GUI.


## Licenza

Questo progetto è concesso in licenza con la licenza MIT. Vedi il file `LICENSE` per ulteriori dettagli.
```
