from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.spinner import Spinner
from kivy.app import App


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
