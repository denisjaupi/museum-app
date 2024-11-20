from database.db_connection import DBConnection

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

class FooterField(BoxLayout):

    def __init__(self, **kwargs):
        super(FooterField, self).__init__(**kwargs)



class Card(ButtonBehavior, BoxLayout):
    title = StringProperty('')  # Titolo dell'opera
    description = StringProperty('')  # Descrizione dell'opera
    image_source = StringProperty('')  # Percorso dell'immagine
    opera_id = NumericProperty(0)  # ID dell'opera, deve essere un numero (int o float)

    def __init__(self, title, description, image_source, opera_id, add_operas_screen, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.add_operas_screen = add_operas_screen
        self.title = title
        self.description = description
        self.image_source = image_source
        self.opera_id = opera_id

        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 5

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Carica l'immagine dal path
        self.image = Image(source=self.image_source, allow_stretch=True, keep_ratio=True, size_hint_y=0.8)

        # Aggiorna il Label per mostrare il titolo invece della descrizione
        self.label = Label(
            text=self.title,  # Cambiato a self.title per mostrare il titolo
            font_name='src/app/utils/Montserrat-Bold.ttf',
            halign='center',
            valign='top',
            size_hint_y=0.2,
            text_size=(self.width, None),
            color=[0, 0, 0, 1],
            shorten=True,
            shorten_from='right'
        )

        self.add_widget(self.image)
        self.add_widget(self.label)

        # Lega il comportamento di clic e dimensione
        self.bind(on_touch_down=self.on_card_click)
        self.bind(size=self._update_rect)
        self.bind(pos=self._update_rect)

    def on_card_click(self, instance, touch):
        """Quando si clicca sulla card, si va alla pagina dell'opera con il popup."""
        if self.collide_point(*touch.pos):
            # Crea il layout per il popup
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

            # Recupera i dettagli dell'opera dal database (incluso l'autore)
            db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
            db.connect()

            query_details = f"""
                SELECT titolo->'{self.add_operas_screen.current_language}', descrizione->'{self.add_operas_screen.current_language}', autore, percorso_immagine
                FROM opere_d_arte
                WHERE id = {self.opera_id};
            """
            result = db.execute_query(query_details)
            db.close()

            if result:
                title, description, author, image_path = result[0]

                # Layout orizzontale per le immagini
                images_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=200, spacing=10)

                # Recupera le immagini associate a questa opera (con immagine_id e percorso_immagine)
                db.connect()
                query_images = f"""
                    SELECT immagine_id, percorso_immagine
                    FROM opere_d_arte 
                    WHERE id = {self.opera_id};
                """
                images = db.execute_query(query_images)
                db.close()

                # Usa un GridLayout per i pulsanti in modo che si distribuiscano orizzontalmente
                buttons_layout = GridLayout(cols=len(images), size_hint_y=None, height=40, spacing=10)  
                for image in images:
                    image_id = image[0]  # immagine_id
                    image_button = Button(
                        text=f"Immagine {image_id}",  # Mostra il 'immagine_id' come testo del bottone
                        size_hint_x=1,  # I pulsanti occupano tutto lo spazio orizzontale disponibile
                        on_release=lambda btn, img_id=image_id: self.on_image_button_click(img_id)
                    )
                    buttons_layout.add_widget(image_button)

                    # Aggiungi le immagini al layout
                    opera_image = Image(source=image[1], allow_stretch=True, height=150, width=150)  # usa percorso_immagine per il source
                    images_layout.add_widget(opera_image)

                layout.add_widget(buttons_layout)  # Aggiungi i pulsanti sopra le immagini
                layout.add_widget(images_layout)   # Aggiungi le immagini sotto i pulsanti

                # Layout per Titolo e Autore (affiancati)
                title_author_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
                
                # Etichetta per il titolo
                title_label = Label(text="Titolo", size_hint_x=None, width=80)
                title_author_layout.add_widget(title_label)

                # Campo di input per il titolo
                title_input = TextInput(text=title, hint_text="Modifica il titolo", size_hint_x=1, height=40)
                title_author_layout.add_widget(title_input)

                # Etichetta per l'autore
                author_label = Label(text="Autore", size_hint_x=None, width=80)
                title_author_layout.add_widget(author_label)

                # Campo di input per l'autore
                author_input = TextInput(text=author, hint_text="Autore dell'opera", size_hint_x=1, height=40)
                title_author_layout.add_widget(author_input)

                layout.add_widget(title_author_layout)

                # Etichetta per la descrizione
                description_label = Label(text="Descrizione", size_hint_y=None, height=40)
                layout.add_widget(description_label)

                # Campo di input per la descrizione
                description_input = TextInput(text=description, hint_text="Modifica descrizione", multiline=True, size_hint_y=None, height=150)
                layout.add_widget(description_input)

                # Bottone per salvare le modifiche
                save_button = Button(
                    text="Salva modifiche",
                    size_hint_y=None,
                    height=50
                )
                save_button.bind(on_release=lambda x: self.save_changes(title_input.text, author_input.text, description_input.text, self.popup))
                layout.add_widget(save_button)

                # Bottone per chiudere il popup
                close_button = Button(
                    text="Chiudi",
                    size_hint_y=None,
                    height=50
                )
                close_button.bind(on_release=lambda x: self.popup.dismiss())
                layout.add_widget(close_button)

                # Crea il popup
                self.popup = Popup(
                    title="Dettagli Opera",
                    content=layout,
                    size_hint=(0.8, 0.9)  # Aggiusta la dimensione del popup
                )
                self.popup.open()

    def close_popup(self):
        """Chiude il popup quando si cambia schermata."""
        if self.popup:
            self.popup.dismiss()

    def on_image_button_click(self, image_id):
        """Gestisci il click su uno dei pulsanti delle immagini."""
        print(f"Immagine selezionata: {image_id}")

        # Recupera l'id dell'opera e il percorso dell'immagine selezionata
        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        db.connect()

        # Query per ottenere id, immagine_id e percorso_immagine
        query = f"""
            SELECT id, immagine_id, percorso_immagine
            FROM opere_d_arte
            WHERE immagine_id = {image_id};
        """
        result = db.execute_query(query)
        db.close()

        if result:
            opera_id, immagine_id, percorso_immagine = result[0]
 
            # Passa le informazioni alla schermata "aggiungi_dettagli"
            add_details_screen = self.add_operas_screen.manager.get_screen('aggiungi_dettagli')
            add_details_screen.set_image_data(opera_id, immagine_id, percorso_immagine)

            # Chiudi il popup se è aperto
            self.close_popup()

            App.get_running_app().root.current = 'aggiungi_dettagli'


    def save_changes(self, title, author, description, popup):
        """Salva le modifiche nel database"""
        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        db.connect()

        # Query di aggiornamento
        update_query = f"""
            UPDATE opere_d_arte 
            SET titolo = '{title}', autore = '{author}', descrizione = '{description}'
            WHERE id = {self.opera_id};
        """
        db.execute_query(update_query)
        db.commit()  # Applica le modifiche
        db.close()

        # Chiudi il popup dopo aver salvato le modifiche
        popup.dismiss()

    def _update_rect(self, instance, value):
        """Assicura che la rect e il testo si aggiornino correttamente durante i cambiamenti di dimensione"""
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class AddOperasScreen(Screen):
    card_data = ListProperty([])  # La lista delle opere d'arte verrà aggiornata dinamicamente
    visible_cards = 3
    current_index = 0
    current_language = 'it'  # Lingua predefinita (italiano)

    def __init__(self, **kwargs):
        super(AddOperasScreen, self).__init__(**kwargs)
        self.fetch_opere_d_arte()  # Recupera i dati dal database
        self.update_cards()

            

    def fetch_opere_d_arte(self):
        """Recupera i dati delle opere d'arte dal database e aggiorna card_data."""
        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        db.connect()  # Connessione al database

        # Modifica la query per includere solo le opere con id_immagine=1
        query = f"""
            SELECT id, titolo->'{self.current_language}', descrizione->'{self.current_language}', percorso_immagine 
            FROM opere_d_arte 
            WHERE immagine_id = 1;
        """
        results = db.execute_query(query)

        if results:
            # Aggiungi l'ID dell'opera alla card_data
            self.card_data = [
                {'id': row[0], 'title': row[1], 'description': row[2], 'image_source': row[3]} for row in results
            ]
        db.close()  # Chiudi la connessione



    def update_cards(self):
        self.ids.card_grid.clear_widgets()
        end_index = self.current_index + self.visible_cards
        cards_to_display = self.card_data[self.current_index:end_index]

        for data in cards_to_display:
            # Assicurati che title e description siano stringhe
            title = str(data['title']) if not isinstance(data['title'], str) else data['title']
            description = str(data['description']) if not isinstance(data['description'], str) else data['description']
            image_source = data['image_source']  # Il percorso dell'immagine
            opera_id = data.get('id', '') # ID dell'opera

            # Passa il titolo, la descrizione e l'immagine alla Card
            card = Card(title=title, description=description, image_source=image_source, opera_id=opera_id, add_operas_screen=self)
            self.ids.card_grid.add_widget(card)

        empty_slots = self.visible_cards - len(cards_to_display)
        for _ in range(empty_slots):
            self.ids.card_grid.add_widget(Widget())

    def scroll_left(self):
        if self.current_index > 0:
            self.current_index -= self.visible_cards
            self.update_cards()

    def scroll_right(self):
        if self.current_index + self.visible_cards < len(self.card_data):
            self.current_index += self.visible_cards
            self.update_cards()
