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
from kivy.uix.spinner import Spinner
from kivy.lang import Builder


class FooterField(BoxLayout):
    text = StringProperty('')  # Proprietà 'text' per il TextInput

    def __init__(self, **kwargs):
        super(FooterField, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = "100dp"

    def update_text(self, new_text):
        """Metodo per aggiornare il testo nel TextInput"""
        self.text = new_text  # Imposta il nuovo testo sulla proprietà 'text'


class Card(ButtonBehavior, BoxLayout):
    title = StringProperty('')  # Titolo dell'opera
    description = StringProperty('')  # Descrizione dell'opera
    image_source = StringProperty('')  # Percorso dell'immagine
    opera_id = NumericProperty(0)  # ID dell'opera, deve essere un numero (int o float)

    def __init__(self, title, description, image_source, opera_id, gallery_screen, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.gallery_screen = gallery_screen
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
            font_name = 'src/app/utils/Montserrat-Bold.ttf',
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

        Window.bind(mouse_pos=self.on_card_hover)

    def on_card_hover(self, instance, touch):
        """Mostra la descrizione nel footer quando la card è hoverata"""
        if self.collide_point(*Window.mouse_pos):
            footer = self.gallery_screen.ids.footer
            if footer:
                footer.text = self.description  # Imposta la proprietà 'text' per aggiornare il footer

    def on_card_click(self, instance, touch):
        """Quando si clicca sulla card, si va alla pagina dell'opera"""
        if self.collide_point(*touch.pos):  # Verifica se il punto di tocco è dentro la card
            opera_screen = self.gallery_screen.manager.get_screen('opera')
            opera_screen.image_source = self.image_source
            opera_screen.opera_id = self.opera_id  
            opera_screen.current_language = self.gallery_screen.current_language
            App.get_running_app().root.current = 'opera'  

    def _update_rect(self, instance, value):
        """Assicura che la rect e il testo si aggiornino correttamente durante i cambiamenti di dimensione"""
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class GalleryScreen(Screen):
    card_data = ListProperty([])  # La lista delle opere d'arte verrà aggiornata dinamicamente
    visible_cards = 3
    current_index = 0
    current_language = 'it'  # Lingua predefinita (italiano)

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)
        self.fetch_opere_d_arte()  # Recupera i dati dal database
        self.update_cards()

        # Ascolta il cambiamento di lingua dallo Spinner
        self.bind(on_enter=self.bind_spinner)

    def bind_spinner(self, *args):
        self.ids.language_spinner.bind(text=self.on_language_change)

    def on_language_change(self, instance, value):
        self.current_language = value
        print(f"Language changed to: {value}")
        # Logica per aggiornare la lingua nell'app

    def on_leave(self):
        """Metodo per azzerare lo stato quando si lascia la schermata"""
        footer = self.ids.footer  # Ottieni il footer dalla vista
        if footer:
            footer.update_text('')
            

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
            card = Card(title=title, description=description, image_source=image_source, opera_id=opera_id, gallery_screen=self)
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

    def on_language_change(self, spinner, language):
        """Metodo che viene chiamato quando cambia la lingua nello spinner"""
        if language == 'IT':
            self.current_language = 'it'
        elif language == 'EN':
            self.current_language = 'en'
        # Aggiorna le card e la descrizione quando cambia la lingua
        self.fetch_opere_d_arte()  # Ricarica i dati delle opere d'arte nella nuova lingua
        self.update_cards()  # Ricarica le card con la lingua aggiornata
        self.update_footer_description()  # Aggiorna la descrizione nel footer

    def update_footer_description(self):
        """Recupera e aggiorna la descrizione nel footer per la lingua selezionata"""
        if len(self.card_data) > 0:
            first_card = self.card_data[0]  # Usa la prima card per esempio
            footer = self.ids.footer  # Ottieni il riferimento al footer
            if footer:
                footer.update_text(first_card['description'])  # Aggiorna il testo del footer