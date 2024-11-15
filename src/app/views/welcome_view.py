from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from PIL import Image as PILImage
from kivy.core.image import Image as CoreImage
import io
from kivy.properties import StringProperty


class GIFImage(Image):
    gif_path = StringProperty()  # Definisci gif_path come proprietà

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gif_frames = []
        self.current_frame = 0

        # Controlla se gif_path è impostato
        if self.gif_path:
            self.load_gif(self.gif_path)

    def on_gif_path(self, instance, value):
        # Carica la GIF quando gif_path cambia
        self.load_gif(value)

    def load_gif(self, path, frame_rate=30):
        # Carica i frame della GIF
        self.gif_frames = []
        self.current_frame = 0
        try:
            pil_image = PILImage.open(path)
            while True:
                frame = pil_image.copy()
                frame_data = io.BytesIO()
                frame.save(frame_data, format="PNG")
                frame_data.seek(0)
                self.gif_frames.append(CoreImage(frame_data, ext="png").texture)
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass

        if self.gif_frames:
            self.texture = self.gif_frames[0]
            # Calcola l'intervallo di aggiornamento dei frame utilizzando il frame rate specificato
            interval = 1 / frame_rate
            Clock.schedule_interval(self.update_frame, interval)

    def update_frame(self, dt):
        if self.gif_frames:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.texture = self.gif_frames[self.current_frame]
# class ContentWidget(BoxLayout):
#     # Proprietà per il testo, immagine e dimensione del font del testo principale
#     text_content = StringProperty("Il primo palazzo dei Medici, dove vissero Cosimo il Vecchio e Lorenzo il Magnifico e lavorarono artisti come Donatello, Michelangelo, Paolo Uccello, Benozzo Gozzoli e Botticelli.")
#     subtext_content = StringProperty("Dove tutto ebbe inizio.")
#     image_source = StringProperty("utils/IMG_Test2.png")
    
#     # Proprietà per la dimensione del font del testo principale
#     main_font_size = NumericProperty(24)  # Font standard di base

#     def __init__(self, **kwargs):
#         super(ContentWidget, self).__init__(**kwargs)
#         self.orientation = 'horizontal'
        
#         # Layout per la colonna di testo (sinistra)
#         text_layout = BoxLayout(orientation='vertical', padding=[self.width * 0.1, self.height * 0.2])
        
#         # Label per il testo principale
#         self.text_label = Label(
#             text=self.text_content,
#             font_size=self.main_font_size,  # Font standard
#             text_size=(self.width * 0.8, None),  # Permette di andare a capo
#             halign='center',
#             valign='bottom',
#             color=[0, 0, 0, 1],
#             padding=[100, 0, 100, 0]  # Aggiungi spazio sotto il testo
#         )
#         # Ridimensionamento automatico della larghezza
#         self.text_label.bind(size=self.text_label.setter('text_size'))
#         self.text_label.bind(texture_size=self.text_label.setter('size'))
        
#         # Aggiunta della label del testo principale
#         text_layout.add_widget(self.text_label)

#         # Label per il sottotesto, proporzionato al testo principale
#         self.subtext_label = Label(
#             text=self.subtext_content,
#             font_size=self.main_font_size * 1.25,  # Proporzione del font del sottotesto
#             text_size=(self.width * 0.8, None),
#             halign='center',
#             valign='top',
#             color=[0, 0, 0, 1]
#         )
#         # Ridimensionamento automatico della larghezza
#         self.subtext_label.bind(size=self.subtext_label.setter('text_size'))
#         self.subtext_label.bind(texture_size=self.subtext_label.setter('size'))
        
#         # Aggiunta della label del sottotesto
#         text_layout.add_widget(self.subtext_label)
        
#         # Layout per l'immagine (destra)
#         image_layout = BoxLayout()
#         self.image = Image(
#             source=self.image_source,
#             allow_stretch=True,
#             keep_ratio=True
#         )
#         image_layout.add_widget(self.image)
        
#         # Aggiunta dei layout al widget principale
#         self.add_widget(text_layout)
#         self.add_widget(image_layout)


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        # Creazione e aggiunta del ContentWidget alla schermata
        # self.content_widget = ContentWidget()
        # self.ids.main_grid.add_widget(self.content_widget)
