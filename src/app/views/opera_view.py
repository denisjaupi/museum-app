from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


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


class OperaScreen(Screen):
    image_source = StringProperty('')
    annotations = ListProperty([])

    def on_pre_enter(self, *args):
        """Metodo chiamato prima che la schermata venga mostrata; carica i dettagli dell'opera"""
        self.load_opera_details()  # Carica immagine e annotazioni
        self.update_image()
        self.add_annotations()

        # Stampa le dimensioni per il debug
        print("Dimensioni del BoxLayout principale:", self.size)
        print("Dimensioni del FooterField:", self.ids.footer_field.size)
        print("Dimensioni del Scatter:", self.ids.opera_scatter.size)
        print("Dimensioni dell'immagine:", self.ids.opera_image.size)



    def load_opera_details(self):
        """Carica i dettagli dell'opera, come immagine e annotazioni."""
        # Imposta il percorso dell'immagine
        self.image_source = 'utils/IMG_Test.jpg'

        # Carica le annotazioni (coordinate e descrizioni)
        self.annotations = [
            {'x': 100, 'y': 100, 'text': 'Dettaglio 1: Descrizione del dettaglio.'},
            {'x': 200, 'y': 200, 'text': 'Dettaglio 2: Un altro dettaglio interessante.'},
            # Aggiungi altre annotazioni
        ]

    def update_image(self):
        """Aggiorna l'immagine nel widget Image e la adatta allo spazio disponibile in modo proporzionato."""
        self.ids.opera_image.source = self.image_source
        self.ids.opera_image.reload()

        # Ottieni dimensioni del BoxLayout principale e del FooterField in pixel
        main_layout_width, main_layout_height = self.ids.image_box.size
        footer_height = self.ids.footer_field.height
        available_height = main_layout_height - footer_height

        # Imposta lo Scatter per usare tutto lo spazio disponibile
        self.ids.opera_scatter.size = (main_layout_width, available_height)
        scatter_width, scatter_height = self.ids.opera_scatter.size

        # Dimensioni della texture dell'immagine in pixel
        img_width, img_height = self.ids.opera_image.texture_size

        # Fattore di scala proporzionato (ad esempio 2 o 3)
        scale_factor = min(scatter_width / img_width, scatter_height / img_height) * 14

        # Calcola le nuove dimensioni dell'immagine con il fattore moderato
        new_width = img_width * scale_factor
        new_height = img_height * scale_factor
        self.ids.opera_image.size = (new_width, new_height)

        # Centra l'immagine nello Scatter
        self.ids.opera_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Debug: stampa per verificare le dimensioni finali
        print(f"Image Size (Texture): {img_width}x{img_height}")
        print(f"Scaled Image Size: {new_width}x{new_height}")
        print(f"Scatter Size (Box): {scatter_width}x{scatter_height}")
        print(f"Dimensioni del BoxLayout principale: {main_layout_width}x{main_layout_height}")
        print(f"Dimensioni del FooterField: {footer_height}")
        print(f"Dimensioni dell'immagine: {self.ids.opera_image.size}")

    def add_annotations(self):
        """Aggiunge le box interattive di annotazione sopra l'immagine"""
        scatter = self.ids.opera_scatter

        # Rimuove annotazioni precedenti (se ce ne sono)
        for child in scatter.children[:]:
            if isinstance(child, Button):
                scatter.remove_widget(child)

        # Aggiunge ogni annotazione come un bottone posizionabile
        for annot in self.annotations:
            btn = Button(
                size_hint=(None, None),
                size=(50, 50),
                pos=(annot['x'], annot['y']),
                background_color=(1, 0, 0, 0.5),
                on_release=lambda btn, txt=annot['text']: self.show_annotation_text(txt)
            )
            scatter.add_widget(btn)

    def show_annotation_text(self, text):
        """Aggiorna il testo nella FooterField con il dettaglio dell'annotazione selezionata"""
        self.ids.footer_field.update_text(text)
