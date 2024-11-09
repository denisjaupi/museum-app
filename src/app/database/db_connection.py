# db_connection.py
import psycopg2

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

    def execute_query(self, query, params=None):
        """Esegue una query e restituisce i risultati."""
        if self.connection and self.cursor:
            try:
                self.cursor.execute(query, params)
                return self.cursor.fetchall()
            except Exception as error:
                print(f"Errore nell'esecuzione della query: {error}")
                return None
        else:
            print("Connessione non stabilita.")
            return None

    def close(self):
        """Chiude la connessione al database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connessione al database chiusa.")
