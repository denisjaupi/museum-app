from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from database.db_connection import DBConnection

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
        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()

        # Query per ottenere l'immagine principale, titolo, autore e descrizione dell'opera
        query_opera = """
            SELECT immagine_principale, titolo->>'{lang}', autore, descrizione->>'{lang}'
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

    def on_back_button_press(self):
        """Gestisce la pressione del pulsante info_butt e naviga alla schermata InfoOperaScreen."""
        app = App.get_running_app()
        opera_screen = app.root.get_screen('opera')  # Ottieni InfoOperaScreen direttamente da ScreenManager
        
        # Passa i parametri a opera_screen
        opera_screen.image_source = self.image_source
        opera_screen.opera_id = self.opera_id
        opera_screen.current_language = self.current_language
        
        # Cambia la schermata corrente a 'opera'
        app.root.current = 'opera'
