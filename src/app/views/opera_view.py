from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


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
    image_source = StringProperty('')  # Proprietà per l'immagine da visualizzare

    def on_enter(self):
        # Aggiorna l'immagine quando si entra nella schermata
        self.ids.opera_image.source = self.image_source
        self.ids.opera_image.reload()  # Ricarica l'immagine per assicurarsi che venga visualizzata
