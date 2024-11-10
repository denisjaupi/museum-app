from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from database.db_connection import DBConnection


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
        print(f"Caricando l'immagine da: {source}")
        self.image_source = source
        self.image.source = self.image_source
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
    opera_id = NumericProperty(0)
    current_language = StringProperty('it')  

    # Aggiungiamo variabili per gestire l'elenco delle immagini e l'indice corrente
    image_paths = ListProperty([])  # Lista dei percorsi delle immagini per l'opera
    current_image_index = NumericProperty(0)  # Indice dell'immagine corrente

    def on_pre_enter(self):
        self.load_opera_images()
        self.update_display()
        
    def on_leave(self):
        """Quando la schermata sta per essere lasciata"""
        # Resetta lo stato dell'immagine e delle annotazioni
        self.image_source = ''
        self.annotations.clear()
        self.viewer.clear_annotations()
        self.ids.footer_field.update_text('')  # Azzera il testo nel footer


    def load_opera_images(self):
        """Carica l'immagine principale e tutte le immagini correlate a questa opera dal database."""
        if not self.opera_id:
            return

        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()

        # Query per ottenere l'immagine principale dell'opera
        query_main_image = """
            SELECT immagine_principale 
            FROM opere_d_arte 
            WHERE id = %s
        """
        result_main_image = db.execute_query(query_main_image, (self.opera_id,))
        
        # Aggiungi l'immagine principale come primo elemento nella lista `image_paths`
        if result_main_image:
            main_image_path = result_main_image[0][0]
            self.image_paths = [main_image_path]  # Inizializza `image_paths` con l'immagine principale

        # Query per ottenere tutte le immagini correlate all'opera
        query_related_images = """
            SELECT percorso 
            FROM immagini_opera 
            WHERE opera_id = %s
            ORDER BY id  -- Assicura un ordine costante, ad esempio per id
        """
        result_related_images = db.execute_query(query_related_images, (self.opera_id,))
        db.close()

        # Aggiungi i percorsi delle immagini correlate a `image_paths`
        related_image_paths = [row[0] for row in result_related_images]
        self.image_paths.extend(related_image_paths)  # Aggiunge le immagini correlate alla lista

        # Imposta l'indice corrente su 0 (prima immagine, che è quella principale)
        self.current_image_index = 0

        # Carica anche le annotazioni per la prima immagine (se necessario)
        self.load_annotations_for_current_image()

    def load_annotations_for_current_image(self):
        """Carica le annotazioni relative all'immagine corrente"""
        if not self.image_paths:
            return
        
        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()
        
        # Esempio di query per le annotazioni specifiche dell'opera; adattare se necessario
        query_annotations = f"""
            SELECT titolo->>'{self.current_language}', testo->>'{self.current_language}', coordinata_x, coordinata_y 
            FROM dettagli_opera 
            WHERE opera_id = %s
        """
        result_annotations = db.execute_query(query_annotations, (self.opera_id,))
        db.close()
        
        if result_annotations:
            self.annotations = [
                {'rel_x': row[2], 'rel_y': row[3], 'text': f"{row[0]}\n {row[1]}"}
                for row in result_annotations
            ]
        else:
            self.annotations = []

    def show_previous_image(self):
        """Mostra l'immagine precedente nella lista, se disponibile."""
        if not self.image_paths:
            return

        # Decrementa l'indice e torna all'ultimo elemento se siamo a inizio lista
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.image_source = self.image_paths[self.current_image_index]

        # Aggiorna la visualizzazione
        self.update_display()

    def show_next_image(self):
        """Mostra l'immagine successiva nella lista, se disponibile."""
        if not self.image_paths:
            return

        # Incrementa l'indice e torna al primo elemento se siamo alla fine della lista
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.image_source = self.image_paths[self.current_image_index]
        
        # Aggiorna la visualizzazione
        self.update_display()

    def show_annotation_text(self, text):
        """Mostra il testo dell'annotazione nel footer"""
        self.ids.footer_field.update_text(text) 

    def update_display(self):
        """Aggiorna il visualizzatore dell'opera con l'immagine corrente e le annotazioni."""
        if self.viewer:
            
            # Carica l'immagine corrente
            self.viewer.load_image(self.image_source)
            
            # Pulisce le annotazioni esistenti
            self.viewer.clear_annotations()

            # Aggiunge le annotazioni
            for annot in self.annotations:
                self.viewer.add_annotation(
                    annot['rel_x'],
                    annot['rel_y'],
                    annot['text'],
                    self.show_annotation_text
                )
