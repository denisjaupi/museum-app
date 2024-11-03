from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class FooterField(BoxLayout):
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
        self.text_input.text = new_text


class OperaImageViewer(RelativeLayout):
    """Visualizzatore dell'immagine dell'opera con annotazioni posizionate sopra"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Crea un Scatter per l'immagine
        self.scatter = Scatter(
            do_rotation=False,
            do_translation=True,
            do_scale=True,
            scale_min=1,
            scale_max=3,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.scatter)

        # Crea un FloatLayout all'interno dello scatter per contenere l'immagine e le annotazioni
        self.content = FloatLayout(size_hint=(1, 1))
        self.scatter.add_widget(self.content)

        # Crea l'immagine all'interno del content
        self.image = Image(
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.content.add_widget(self.image)
        
        self.layout_triggered = False
        self.annotations = []

    def load_image(self, source):
        """Carica una nuova immagine"""
        self.image.source = source
        self.image.reload()
        Clock.schedule_once(lambda dt: self.update_layout(), 0.1)
        
    def update_layout(self, *args):
        """Aggiorna il layout e riposiziona le annotazioni"""
        if not self.image.texture or self.layout_triggered:
            return
            
        self.layout_triggered = True
        
        # Calcola le dimensioni target dell'immagine
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
            
        self.scatter.size = (target_width, target_height)
        self.content.size = (target_width, target_height)
        self.image.size = (target_width, target_height)
        
        if self.parent:
            self.scatter.pos = (
                (self.parent.width - target_width) / 2,
                (self.parent.height - target_height) / 2
            )

        # Riposiziona le annotazioni passando self.parent.annotations
        if hasattr(self.parent, 'annotations'):
            self.reposition_annotations(self.parent.annotations)

        self.layout_triggered = False

    def reposition_annotations(self, annotations):
        """Aggiorna la posizione delle annotazioni"""
        for btn in self.annotations:
            self.content.remove_widget(btn)
        self.annotations.clear()
        
        for annot in annotations:
            self.add_annotation(annot['rel_x'], annot['rel_y'], annot['text'], self.parent.show_annotation_text)

    def clear_annotations(self):
        """Rimuove tutte le annotazioni esistenti"""
        for btn in self.annotations:
            self.content.remove_widget(btn)
        self.annotations.clear()
                
    def add_annotation(self, rel_x, rel_y, text, callback):
        """Aggiunge un'annotazione alla posizione relativa specificata"""
        btn = Button(
            text='',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'x': rel_x - 0.025, 'y': rel_y - 0.025},  # Aggiusta per centrare il bottone
            background_color=(1, 0, 0, 0.5),
            on_release=lambda btn: callback(text)
        )
        self.annotations.append(btn)
        self.content.add_widget(btn)


class OperaScreen(Screen):
    image_source = StringProperty('')
    annotations = ListProperty([])
    viewer = ObjectProperty(None)
    
    def on_pre_enter(self):
        self.load_opera_details()
        self.update_display()
        
    def load_opera_details(self):
        self.image_source = 'utils/IMG_Test.jpg'
        self.annotations = [
            {'rel_x': 0.24, 'rel_y': 0.4, 'text': 'Cosimo di Giovanni de Medici: detto il Vecchio o Pater Patriae (Firenze, 27 settembre 1389 – Careggi, 1º agosto 1464) è stato un politico e banchiere italiano, primo signore de facto di Firenze e primo uomo di Stato di rilievo della famiglia Medici.'},
            {'rel_x': 0.32, 'rel_y': 0.4, 'text': 'Piero di Cosimo de Medici: detto il Gottoso (Firenze, 14 giugno 1416 – Firenze, 2 dicembre 1469), è stato un politico italiano, signore de facto di Firenze per cinque anni, dal 1464 al 1469. Figlio primogenito di Cosimo il Vecchio.'},
            {'rel_x': 0.13, 'rel_y': 0.4, 'text': 'Galeazzo Maria Sforza: (Fermo, 14 o 24 gennaio 1444 – Milano, 26 dicembre 1476) fu duca di Milano dal 1466 al 1476, anno in cui fu assassinato nei pressi della chiesa di Santo Stefano per mano di alcuni nobili.'},
            {'rel_x': 0.04, 'rel_y': 0.4, 'text': 'Sigismondo Pandolfo Malatesta: (Brescia, 19 giugno 1417 – Rimini, 9 ottobre 1468) fu signore di Rimini e Fano dal 1432. Considerato dai suoi contemporanei come uno dei più audaci condottieri militari in Italia, partecipò a molte battaglie che caratterizzarono quel periodo.'},
            {'rel_x': 0.44, 'rel_y': 0.3, 'text': 'Carlo de Medici: (1540-1592), figlio illegittimo di Cosimo I de Medici, fu un nobile fiorentino che ricoprì ruoli significativi nella politica toscana, servendo come governatore di Siena e sostenendo le arti, nonostante la sua condizione di illegittimità.'},
            {'rel_x': 0.67, 'rel_y': 0.4, 'text': 'Gaspare: uno dei Magi. Porta in dono la mirra, che essendo legata al culto dei morti è un omaggio all\' umanità di Cristo. Gaspare, come protettore dei Medici (perché la mirra era considerata anche un farmaco), è anche un riferimento al cognome della famiglia Medici. Avrebbe le sembianze idealizzate di Lorenzo de Medici.'}
        ]
            
    def show_annotation_text(self, text):
        print(f"Updating footer text with: {text}")
        self.ids.footer_field.update_text(text)

    def update_display(self):
        self.viewer = self.ids.opera_scatter
        self.viewer.load_image(self.image_source)
        
        self.viewer.clear_annotations()
        
        for annot in self.annotations:
            self.viewer.add_annotation(
                annot['rel_x'],
                annot['rel_y'],
                annot['text'],
                self.show_annotation_text
            )