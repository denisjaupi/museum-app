from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
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

class ContentWidget(BoxLayout):
    # Proprietà per il testo, immagine e dimensione del font del testo principale
    text_content = StringProperty("Il primo palazzo dei Medici, dove vissero Cosimo il Vecchio e Lorenzo il Magnifico e lavorarono artisti come Donatello, Michelangelo, Paolo Uccello, Benozzo Gozzoli e Botticelli.")
    subtext_content = StringProperty("Dove tutto ebbe inizio.")
    image_source = StringProperty("utils/IMG_Test2.png")
    
    # Proprietà per la dimensione del font del testo principale
    main_font_size = NumericProperty(24)  # Font standard di base

    def __init__(self, **kwargs):
        super(ContentWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        
        # Layout per la colonna di testo (sinistra)
        text_layout = BoxLayout(orientation='vertical', padding=[self.width * 0.1, self.height * 0.2])
        
        # Label per il testo principale
        self.text_label = Label(
            text=self.text_content,
            font_size=self.main_font_size,  # Font standard
            text_size=(self.width * 0.8, None),  # Permette di andare a capo
            halign='center',
            valign='bottom',
            color=[0, 0, 0, 1],
            padding=[100, 0, 100, 0]  # Aggiungi spazio sotto il testo
        )
        # Ridimensionamento automatico della larghezza
        self.text_label.bind(size=self.text_label.setter('text_size'))
        self.text_label.bind(texture_size=self.text_label.setter('size'))
        
        # Aggiunta della label del testo principale
        text_layout.add_widget(self.text_label)

        # Label per il sottotesto, proporzionato al testo principale
        self.subtext_label = Label(
            text=self.subtext_content,
            font_size=self.main_font_size * 1.25,  # Proporzione del font del sottotesto
            text_size=(self.width * 0.8, None),
            halign='center',
            valign='top',
            color=[0, 0, 0, 1]
        )
        # Ridimensionamento automatico della larghezza
        self.subtext_label.bind(size=self.subtext_label.setter('text_size'))
        self.subtext_label.bind(texture_size=self.subtext_label.setter('size'))
        
        # Aggiunta della label del sottotesto
        text_layout.add_widget(self.subtext_label)
        
        # Layout per l'immagine (destra)
        image_layout = BoxLayout()
        self.image = Image(
            source=self.image_source,
            allow_stretch=True,
            keep_ratio=True
        )
        image_layout.add_widget(self.image)
        
        # Aggiunta dei layout al widget principale
        self.add_widget(text_layout)
        self.add_widget(image_layout)

    
    
    def update_font_size(self, new_size):
        """Aggiorna la dimensione del font principale e scala il sottotesto di conseguenza."""
        self.main_font_size = new_size
        self.text_label.font_size = self.main_font_size
        self.subtext_label.font_size = self.main_font_size * 1.25  # Proporzione per il sottotesto
    
    def update_content(self, new_text=None, new_subtext=None, new_image_source=None):
        """Metodo per aggiornare il testo e/o l'immagine."""
        if new_text:
            self.text_label.text = new_text
        if new_subtext:
            self.subtext_label.text = new_subtext
        if new_image_source:
            self.image.source = new_image_source

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        # Creazione e aggiunta del ContentWidget alla schermata
        self.content_widget = ContentWidget()
        self.ids.main_grid.add_widget(self.content_widget)
