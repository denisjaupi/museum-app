from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from app.database.db_connection import DBConnection

class InfoOperaScreen(Screen):
    image_source = StringProperty('')
    opera_id = NumericProperty(0)
    current_language = StringProperty('it')

    def on_pre_enter(self):
        """Metodo chiamato quando la schermata diventa visibile. Carica i dati dell'opera."""
        print(f"Immagine: {self.image_source}, Opera ID: {self.opera_id}, Lingua: {self.current_language}")
        self.load_opera_info()

    def load_opera_info(self):
        """Carica i dati dell'opera (immagine, titolo, autore, descrizione) dal database."""
        if not self.opera_id:
            return

        # Connessione al database
        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        db.connect()

        # Query per ottenere l'immagine principale, titolo, autore e descrizione dell'opera
        query_opera = """
            SELECT percorso_immagine, titolo->>'{lang}', autore, descrizione->>'{lang}'
            FROM opere_d_arte 
            WHERE id = %s
        """.format(lang=self.current_language)
        result = db.execute_query(query_opera, (self.opera_id,))

        db.close()

        # Se la query ha restituito risultati, popola i campi della schermata
        if result:
            main_image, title, author, description = result[0]  # Ottieni i dati della prima riga

            # Imposta l'immagine, titolo, autore e descrizione nei rispettivi widget
            self.ids.image_box.source = main_image  # Percorso dell'immagine principale
            self.ids.title_box.text = title
            self.ids.author_box.text = author
            self.ids.description_box.text = description
