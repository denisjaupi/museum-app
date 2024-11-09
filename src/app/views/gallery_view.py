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

class HeaderWidget(BoxLayout):
    logo_source = StringProperty('utils/IMG_Test3.png')

    def __init__(self, **kwargs):
        super(HeaderWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Sezione logo (30%)
        logo_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])
        self.logo_image = Image(source=self.logo_source, allow_stretch=True, keep_ratio=True)
        logo_layout.add_widget(self.logo_image)
        logo_layout.add_widget(BoxLayout(size_hint_x=1))  # Spacer
        self.add_widget(logo_layout)

        # Sezione centrale (40%)
        self.central_layout = BoxLayout(size_hint_x=0.4)
        self.add_widget(self.central_layout)

        # Sezione scelta lingua (30%)
        language_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])
        language_layout.add_widget(BoxLayout(size_hint_x=1))  # Spacer
        self.language_spinner = Spinner(
            text='IT',  # Imposta la lingua predefinita
            values=['IT', 'EN'],  # Le lingue selezionabili
            size_hint_x=None,
            width=100,
            font_size=20,
            color=[1, 1, 1, 1],  # Testo bianco
            background_color=[0.447, 0.106, 0.157, 1],  # Sfondo Bordeaux 
            background_normal='',  # Rimuove lo sfondo normale
            background_down=''  # Rimuove lo sfondo quando è premuto
        )
        language_layout.add_widget(self.language_spinner)
        self.add_widget(language_layout)

    def update_logo(self, new_logo_path):
        self.logo_source = new_logo_path
        self.logo_image.source = self.logo_source
        self.logo_image.reload()

class FooterField(BoxLayout):
    text = StringProperty("")

    def __init__(self, **kwargs):
        super(FooterField, self).__init__(**kwargs)
        self.text_input = TextInput(
            hint_text='',
            background_color=[0.447, 0.106, 0.157, 1],
            foreground_color=[1, 1, 1, 1],
            font_size=36,
            multiline=True,
            readonly=True,
            size_hint=(1, 1),
            text=self.text
        )
        self.add_widget(self.text_input)

    def update_text(self, new_text):
        self.text_input.text = new_text


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
        self.opera_id = opera_id  # Non è più necessario convertire in stringa

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
            font_size=23,
            padding=[20, 20],
            halign='left',
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
                footer.update_text(self.description)  # Mostra la descrizione completa nel footer

    def on_card_click(self, instance, touch):
        """Quando si clicca sulla card, si va alla pagina dell'opera"""
        if self.collide_point(*touch.pos):  # Verifica se il punto di tocco è dentro la card
            opera_screen = self.gallery_screen.manager.get_screen('opera')
            opera_screen.image_source = self.image_source

            # Passa l'opera_id alla schermata OperaScreen
            opera_screen.opera_id = self.opera_id  # Non è più necessario convertire in stringa
            App.get_running_app().root.current = 'opera'  # Cambia schermata a 'opera'

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
        self.ids.header_widget.language_spinner.bind(text=self.on_language_change)

    def fetch_opere_d_arte(self):
        """Recupera i dati delle opere d'arte dal database e aggiorna card_data."""
        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()  # Connessione al database

        # Modifica la query per includere anche l'ID dell'opera
        query = f"""
            SELECT id, titolo->'{self.current_language}', descrizione->'{self.current_language}', immagine_principale 
            FROM opere_d_arte;
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
            footer = self.ids.footer
            if footer:
                footer.update_text(first_card['description'])
