import psycopg2
import json

class DBConnection:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Esegue la connessione al database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connessione al database riuscita.")
        except Exception as error:
            print("Errore durante la connessione al database:", error)
            self.cursor = None
            self.connection = None

    def execute_query(self, query, params=None, commit=False):
        """Esegue una query (SELECT o DML) e restituisce i risultati."""
        if self.connection and self.cursor:
            try:
                # Esegui la query
                self.cursor.execute(query, params)
                
                # Se la query è di lettura (SELECT), restituisci i risultati
                if query.strip().lower().startswith("select"):
                    return self.cursor.fetchall()

                # Se è una query di modifica, effettua il commit (se richiesto)
                if commit:
                    self.connection.commit()

                return None  # Nessun risultato da restituire per DML (INSERT, UPDATE, DELETE)
            except Exception as error:
                print(f"Errore nell'esecuzione della query: {error}")
                self.connection.rollback()  # Ripristina in caso di errore
                return None
        else:
            print("Connessione non stabilita.")
            return None

    def insert_opera(self, titolo, autore, descrizione, immagine_principale):
        """Inserisce una nuova opera d'arte nella tabella opere_d_arte."""
        query = """
        INSERT INTO opere_d_arte (titolo, autore, descrizione, immagine_principale)
        VALUES (%s, %s, %s, %s)
        """
        params = (json.dumps(titolo), autore, json.dumps(descrizione), immagine_principale)
        self.execute_query(query, params, commit=True)

    # Funzione insert_user con commit esplicito
    def insert_user(self, username, password_hash):
        """Inserisce un nuovo utente nel database."""
        query = """
        INSERT INTO login (username, password_hash)
        VALUES (%s, %s)
        """
        self.execute_query(query, (username, password_hash), commit=True)
        self.connection.commit()  

    def get_user_by_username(self, username):
        """Verifica se un utente esiste già nel database."""
        query = """
        SELECT * FROM login WHERE username = %s
        """
        return self.execute_query(query, (username,))
    
    def get_password_hash(self, username):
        """Recupera l'hash della password per un determinato nome utente."""
        query = """
        SELECT password_hash FROM login WHERE username = %s
        """
        result = self.execute_query(query, (username,))
        if result:
            return result[0][0]  # Restituisce l'hash della password
        return None

    def get_annotations_for_image(self, immagine_id, language='it'):
        """Recupera tutte le annotazioni per una specifica immagine e lingua."""
        query = """
        SELECT titolo->>%s, testo->>%s, coordinata_x, coordinata_y
        FROM dettagli_opera
        WHERE immagine_id = %s
        """
        params = (language, language, immagine_id)
        return self.execute_query(query, params)


    def insert_annotation(self, id, immagine_id, titolo, testo, coordinata_x, coordinata_y):
        """Inserisce una nuova annotazione nella tabella dettagli_opera."""
        query = """
        INSERT INTO dettagli_opera (id, immagine_id, titolo, testo, coordinata_x, coordinata_y)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Rimuovi json.dumps e passa i dizionari direttamente
        params = (id, immagine_id, titolo, testo, coordinata_x, coordinata_y)
        self.execute_query(query, params, commit=True)



    def close(self):
        """Chiude la connessione al database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connessione al database chiusa.")
