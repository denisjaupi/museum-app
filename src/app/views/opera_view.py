from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.clock import Clock


class FooterField(BoxLayout):
    """Widget per il campo di testo a piè di pagina"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_input = TextInput(
            hint_text='',
            background_color=[0.447, 0.106, 0.157, 1],
            foreground_color=[1, 1, 1, 1],
            font_size=36,
            multiline=True,
            readonly=True,
            size_hint=(1, 1)
        )
        self.add_widget(self.text_input)

    def update_text(self, new_text):
        """Aggiorna il testo visualizzato"""
        self.text_input.text = new_text


class OperaImageViewer(Scatter):
    """Visualizzatore dell'immagine dell'opera"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_translation = True
        self.do_scale = True
        self.scale_min = 1
        self.scale_max = 3
        
        # Creazione dell'immagine
        self.image = Image(
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.image)
        
        self.layout_triggered = False

    def load_image(self, source):
        """Carica una nuova immagine"""
        self.image.source = source
        self.image.reload()
        Clock.schedule_once(lambda dt: self.update_layout(), 0.1)
        
    def update_layout(self, *args):
        """Gestisce l'aggiornamento del layout in modo più efficiente"""
        if not self.image.texture or self.layout_triggered:
            return
            
        self.layout_triggered = True
        
        container_width = self.parent.width if self.parent else 100
        container_height = self.parent.height if self.parent else 100
        container_ratio = container_width / container_height
        
        image_ratio = self.image.texture.width / self.image.texture.height
        
        if image_ratio > container_ratio:
            target_width = container_width
            target_height = container_width / image_ratio
        else:
            target_height = container_height
            target_width = container_height * image_ratio
            
        self.image.size = (target_width, target_height)
        self.size = (target_width, target_height)
        
        if self.parent:
            self.pos = (
                self.parent.center_x - target_width / 2,
                self.parent.center_y - target_height / 2
            )
        
        self.layout_triggered = False
            
    def on_size(self, *args):
        """Risponde ai cambiamenti di dimensione"""
        Clock.schedule_once(lambda dt: self.update_layout(), 0)

    def clear_annotations(self):
        """Rimuove tutte le annotazioni esistenti"""
        for child in list(self.children):
            if isinstance(child, Button):
                self.remove_widget(child)
                
    def add_annotation(self, x, y, text, callback):
        """Aggiunge un'annotazione alla posizione specificata"""
        # Create a button to act as an annotation
        btn = Button(
            text='',
            size_hint=(None, None),
            size=(50, 50),  # Adjust size if needed
            pos=(x, y),  # Position where you want the annotation
            background_color=(1, 0, 0, 0.5),
            on_release=lambda btn: callback(text)
        )
        # Add the button to the parent layout instead of Scatter
        if self.parent:  # Check if there is a parent layout to add to
            self.parent.add_widget(btn)


class OperaScreen(Screen):
    """Schermata principale per la visualizzazione dell'opera d'arte"""
    image_source = StringProperty('')
    annotations = ListProperty([])
    viewer = ObjectProperty(None)
    
    def on_pre_enter(self):
        """Inizializza la schermata quando viene mostrata"""
        self.load_opera_details()
        self.update_display()
        
    def load_opera_details(self):
        """Carica i dettagli dell'opera e le annotazioni"""
        self.image_source = 'utils/IMG_Test.jpg'
        self.annotations = [
            {'x': 100, 'y': 100, 'text': 'Dettaglio 1: Descrizione del dettaglio.'},
            {'x': 200, 'y': 200, 'text': 'Dettaglio 2: Un altro dettaglio interessante.'}
        ]
        
    def update_display(self):
        """Aggiorna la visualizzazione dell'opera e delle annotazioni"""
        self.viewer = self.ids.opera_scatter
        self.viewer.load_image(self.image_source)
        
        self.viewer.clear_annotations()
        for annot in self.annotations:
            self.viewer.add_annotation(
                annot['x'],
                annot['y'],
                annot['text'],
                self.show_annotation_text
            )
            
    def show_annotation_text(self, text):
        """Mostra il testo dell'annotazione nel footer"""
        print(f"Updating footer text with: {text}")
        self.ids.footer_field.update_text(text)

    def update_display(self):
        """Aggiorna la visualizzazione dell'opera e delle annotazioni"""
        self.viewer = self.ids.opera_scatter
        self.viewer.load_image(self.image_source)
        
        self.viewer.clear_annotations()
        for annot in self.annotations:
            self.viewer.add_annotation(
                annot['x'],
                annot['y'],
                annot['text'],
                self.show_annotation_text
            )