from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


class HeaderWidget(BoxLayout):

    # Proprietà per la sorgente dell'immagine del logo
    logo_source = StringProperty('utils/IMG_Test3.png')  # Logo predefinito

    def __init__(self, **kwargs):
        super(HeaderWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Sezione logo (30%)
        logo_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])

        # Aggiungi l'immagine del logo
        self.logo_image = Image(source=self.logo_source, allow_stretch=True, keep_ratio=True)
        logo_layout.add_widget(self.logo_image)

        # Spacer per occupare lo spazio disponibile a destra
        logo_spacer = BoxLayout(size_hint_x=1)  # Occupare tutto lo spazio disponibile
        logo_layout.add_widget(logo_spacer)

        # Aggiungi il layout del logo al widget principale
        self.add_widget(logo_layout)

        # Sezione centrale (40%)
        self.central_layout = BoxLayout(size_hint_x=0.4)
        self.add_widget(self.central_layout)

        # Sezione scelta lingua (30%)
        language_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])

        # Spacer per occupare lo spazio disponibile a sinistra
        language_spacer = BoxLayout(size_hint_x=1)  # Occupare tutto lo spazio disponibile a sinistra
        language_layout.add_widget(language_spacer)

        # Spinner per la selezione della lingua
        self.language_spinner = Spinner(
            text='IT',  # Imposta la lingua predefinita
            values=['IT', 'EN', 'FR', 'DE'],  # Le lingue selezionabili
            size_hint_x=None,
            width=100,
            font_size=20,
            color=[1, 1, 1, 1],  # Testo bianco
            background_color=[0.447, 0.106, 0.157, 1],  # Sfondo Bordeaux 
            background_normal='',  # Rimuove lo sfondo normale
            background_down=''  # Rimuove lo sfondo quando è premuto
        )
        language_layout.add_widget(self.language_spinner)

        # Aggiungi il layout della lingua all'header
        self.add_widget(language_layout)

    def update_logo(self, new_logo_path):
        """Aggiorna l'immagine del logo."""
        self.logo_source = new_logo_path
        self.logo_image.source = self.logo_source
        self.logo_image.reload()  # Ricarica l'immagine per applicare le modifiche

class FooterField(BoxLayout):
    text = StringProperty("")

    def __init__(self, **kwargs):
        super(FooterField, self).__init__(**kwargs)
        
        # Inizializza il campo TextInput
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
        """Aggiorna il testo del footer."""
        self.text_input.text = new_text

class Card(ButtonBehavior, BoxLayout):
    
    # Lista delle opere (ognuna rappresentata da un dizionario con immagine e descrizione)
    card_data = ListProperty([
        {'image_source': 'IMG_Test.jpg', 'description': "La Cappella dei Magi, affrescata da Benozzo Gozzoli. La Cappella dei Magi, affrescata da Benozzo Gozzoli. La Cappella dei Magi, affrescata da Benozzo Gozzoli. La Cappella dei Magi, affrescata da Benozzo Gozzoli."},
        {'image_source': 'IMG_Test.jpg', 'description': "La Galleria terrena con sculture e stucchi."},
        {'image_source': 'IMG_Test.jpg', 'description': "Gli scavi archeologici restituiscono storia."},
        {'image_source': 'IMG_Test.jpg', 'description': "Una vista panoramica delle collezioni storiche."},

    ])

    visible_cards = 3
    current_index = 0

    """ Classe per le card, estende ButtonBehavior per renderle cliccabili. """
    description = StringProperty('')
    font_size = NumericProperty(36) 

    def __init__(self, image_source, description, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.description = description

        # Imposta l'orientamento della Card e il padding
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 5  # Aggiungi un po' di spazio tra immagine e label

        # Sfondo grigio chiaro per la card
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Colore di sfondo grigio chiaro
            self.rect = Rectangle(pos=self.pos, size=self.size)  # Inizializza il rettangolo

        # Immagine che occupa il 60% dello spazio
        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=True, size_hint_y=0.8)

        self.label = Label(
            text=self.description,
            font_size=self.font_size,
            padding = [20, 20],
            halign='left',
            valign='top',
            size_hint_y=0.4,  # Occupare il 40% dell'altezza
            text_size=(self.width, None),  # Permette di andare a capo
            color=[0, 0, 0, 1],  # Testo nero
            shorten=True,  # Abilita il troncamento
            shorten_from='right'  # Troncamento dal lato destro
        )

        # Aggiungi immagine e label alla card
        self.add_widget(self.image)
        self.add_widget(self.label)

        # Rendi la card cliccabile
        self.bind(on_touch_down=self.on_card_click)
        self.bind(size=self._update_rect)  # Aggiorna il rettangolo quando la dimensione cambia
        self.bind(pos=self._update_rect)  # Aggiorna il rettangolo quando la posizione cambia

        Window.bind(mouse_pos=self.on_card_hover)  # Controlla l'hover del mouse

    def on_card_click(self, instance, touch):
        """ Gestisce il clic sulla card. """
        if self.collide_point(*touch.pos):
            App.get_running_app().root.current = 'opera'
            print(f'Card clicked: {self.description}')

    def on_card_hover(self, instance, touch):
        """Gestisce l'hover della card."""
        app = App.get_running_app()
        # Controlla se footer_text è presente
        if hasattr(app.root.ids, 'footer_text'):
            if self.collide_point(*touch):
                print(f'Card hovered: {self.description}')
                app.root.ids.footer_text.update_text(self.description)
            else:
                app.root.ids.footer_text.update_text("")
        else:
            print("ID footer_text non trovato.")



    def _update_rect(self, instance, value):
        """ Aggiorna la posizione e le dimensioni del rettangolo di sfondo. """
        if hasattr(self, 'rect'):  # Controlla se l'attributo rect esiste
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)  # Aggiorna il text_size della label

class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class GalleryScreen(Screen):
    # Lista delle opere (ognuna rappresentata da un dizionario con immagine e descrizione)
    card_data = ListProperty([
        {'image_source': 'IMG_Test.jpg', 'description': "La Cappella dei Magi, affrescata da Benozzo Gozzoli."},
        {'image_source': 'IMG_Test.jpg', 'description': "La Galleria terrena con sculture e stucchi."},
        {'image_source': 'IMG_Test.jpg', 'description': "Gli scavi archeologici restituiscono storia."},
        {'image_source': 'IMG_Test.jpg', 'description': "Una vista panoramica delle collezioni storiche."},

    ])

    visible_cards = 3
    current_index = 0

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)
        self.update_cards()

    def update_cards(self):
        # Svuota la griglia prima di riempirla di nuovo
        self.ids.card_grid.clear_widgets()

        # Calcola l'indice finale e seleziona le opere da visualizzare
        end_index = self.current_index + self.visible_cards
        cards_to_display = self.card_data[self.current_index:end_index]

        # Aggiungi le card alla griglia
        for data in cards_to_display:
            card = Card(image_source=data['image_source'], description=data['description'])
            self.ids.card_grid.add_widget(card)

        # Aggiungi spazi vuoti per riempire i posti mancanti, se meno di 3 card
        empty_slots = self.visible_cards - len(cards_to_display)
        for _ in range(empty_slots):
            self.ids.card_grid.add_widget(Widget())  # Widget vuoto per riempire gli spazi mancanti

    def scroll_left(self):
        if self.current_index > 0:
            # Diminuisce di 3 l'indice corrente per visualizzare il gruppo precedente
            self.current_index -= self.visible_cards
            self.update_cards()

    def scroll_right(self):
        # Incrementa di 3 l'indice corrente per visualizzare il prossimo gruppo
        if self.current_index + self.visible_cards < len(self.card_data):
            self.current_index += self.visible_cards
            self.update_cards()





