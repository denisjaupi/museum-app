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

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

