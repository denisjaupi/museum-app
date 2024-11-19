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
from kivy.app import App

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
        print(f"Aggiornamento footer con testo: {new_text}")
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
        """Aggiunge un'annotazione alla posizione relativa specificata, con dimensione adattabile"""
        print(f"Aggiunta annotazione: {text} alle coordinate ({rel_x}, {rel_y})")
        
        # Crea il pulsante per l'annotazione
        btn = Button(
            text='',
            size_hint=(None, None),  # Disabilita il ridimensionamento automatico
            background_color=(1, 0, 0, 0.5),
            on_release=lambda btn: callback(text)
        )
        
        # Aggiusta dinamicamente la dimensione del pulsante in base alle dimensioni dell'immagine
        def update_button_size(*args):
            """Aggiorna la dimensione del pulsante in base alla dimensione corrente dell'immagine"""
            base_size = 0.07  # Frazione della larghezza dell'immagine da usare come dimensione del pulsante
            btn.size = (self.image.width * base_size, self.image.height * base_size)
        
        # Aggiorna la dimensione iniziale del pulsante
        update_button_size()
        
        # Lega la funzione di aggiornamento alla variazione delle dimensioni dell'immagine
        self.image.bind(size=update_button_size)
        
        # Posiziona il pulsante
        btn.pos_hint = {'x': rel_x - 0.03, 'y': rel_y - 0.03}  # Centrare il bottone rispetto all'annotazione
        self.annotations.append(btn)
        self.content.add_widget(btn)



class OperaScreen(Screen):
    image_source = StringProperty('')
    annotations = ListProperty([])
    viewer = ObjectProperty(None)
    opera_id = NumericProperty(0)
    current_language = StringProperty('it')  

    image_paths = ListProperty([])  # Lista delle immagini relative all'opera (percorso + immagine_id)
    current_image_index = NumericProperty(0)  # Indice dell'immagine corrente

    def on_pre_enter(self):
        self.load_opera_images()
        self.update_display()
        
    def on_leave(self):
        """Resetta lo stato dell'immagine e delle annotazioni quando si lascia la schermata."""
        self.image_source = ''
        self.annotations.clear()
        self.viewer.clear_annotations()
        self.ids.footer_field.update_text('')
    
    def load_opera_images(self):
        """Carica i dettagli e l'immagine principale dell'opera selezionata."""
        if not self.opera_id:
            print("Errore: opera_id non è impostato.")
            return

        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        try:
            db.connect()

            # Query per ottenere l'immagine principale dell'opera e i dettagli
            query = """
                SELECT id, immagine_id, percorso_immagine
                FROM opere_d_arte
                WHERE id = %s
            """
            result = db.execute_query(query, (self.opera_id,))

            # Debug: stampa il risultato della query
            print(f"Risultato della query opere_d_arte: {result}")

            # Verifica che il risultato non sia vuoto
            if not result:
                print(f"Nessun dato trovato per opera_id {self.opera_id}.")
                self.image_paths = []
            else:
                # Popola image_paths con i dati dell'immagine principale
                self.image_paths = [{'immagine_id': row[1], 'percorso_immagine': row[2]} for row in result]

                # Imposta il primo elemento come immagine corrente
                self.current_image_index = 0
                self.image_source = self.image_paths[0]['percorso_immagine']

                # Carica annotazioni per la prima immagine (se necessario)
                self.load_annotations_for_current_image()

        except Exception as e:
            print(f"Errore durante il caricamento dell'opera_id {self.opera_id}: {e}")
            self.image_paths = []
        finally:
            db.close()


    def load_annotations_for_current_image(self):
        """Carica le annotazioni relative all'immagine corrente."""
        if not self.image_paths or not self.image_paths[self.current_image_index]:
            print("Errore: nessuna immagine caricata o immagine corrente non valida.")
            return

        immagine_id = self.image_paths[self.current_image_index]['immagine_id']
        db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
        try:
            db.connect()

            # Query per ottenere annotazioni specifiche per immagine_id
            query_annotations = f"""
                SELECT titolo->>'{self.current_language}', testo->>'{self.current_language}', coordinata_x, coordinata_y
                FROM dettagli_opera
                WHERE immagine_id = %s
            """
            result_annotations = db.execute_query(query_annotations, (immagine_id,))

            # Debug: stampa il risultato della query
            print(f"Annotazioni trovate per immagine_id {immagine_id}: {result_annotations}")

            # Popola la lista delle annotazioni
            if result_annotations:
                self.annotations = [
                    {'rel_x': row[2], 'rel_y': row[3], 'text': f"{row[0]}\n{row[1]}"}
                    for row in result_annotations
                ]
            else:
                self.annotations = []

        except Exception as e:
            print(f"Errore durante il caricamento delle annotazioni per immagine_id {immagine_id}: {e}")
            self.annotations = []
        finally:
            db.close()


    def show_previous_image(self):
        """Mostra l'immagine precedente nella lista, se disponibile."""
        if not self.image_paths:
            return

        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.image_source = self.image_paths[self.current_image_index]['percorso_immagine']

        # Aggiorna la visualizzazione
        self.annotations.clear()
        self.load_annotations_for_current_image()
        self.update_display()

    def show_next_image(self):
        """Mostra l'immagine successiva nella lista, se disponibile."""
        if not self.image_paths:
            return

        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.image_source = self.image_paths[self.current_image_index]['percorso_immagine']

        # Aggiorna la visualizzazione
        self.annotations.clear()
        self.load_annotations_for_current_image()
        self.update_display()

    def show_annotation_text(self, text):
        """Mostra il testo dell'annotazione nel footer."""
        self.ids.footer_field.update_text(text)

    def update_display(self):
        """Aggiorna il visualizzatore dell'opera con l'immagine corrente e le annotazioni."""
        if self.viewer:
            self.viewer.load_image(self.image_source)  # Carica l'immagine corrente
            self.viewer.clear_annotations()  # Pulisce le annotazioni esistenti
            for annot in self.annotations:
                self.viewer.add_annotation(
                    annot['rel_x'],
                    annot['rel_y'],
                    annot['text'],
                    self.show_annotation_text
                )


    def on_info_button_press(self):
        """Naviga alla schermata InfoOperaScreen con i dettagli dell'immagine corrente."""
        app = App.get_running_app()
        info_screen = app.root.get_screen('info_opera')
        info_screen.image_source = self.image_source
        info_screen.opera_id = self.opera_id
        info_screen.current_language = self.current_language
        app.root.current = 'info_opera'
