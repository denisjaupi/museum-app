from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.lang import Builder

from app.database.db_instance import db_instance


# Classe della schermata AddDetailsScreen
class AddDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Aggiungi variabili per i dati passati
        self.opera_id = None
        self.immagine_id = None
        self.percorso_immagine = None

    def set_image_data(self, opera_id, immagine_id, percorso_immagine):
        """Imposta i dati dell'immagine (id, immagine_id, percorso_immagine)."""
        self.opera_id = opera_id
        self.immagine_id = immagine_id
        self.percorso_immagine = percorso_immagine

    def on_enter(self):
        """Carica l'immagine quando si entra nella schermata."""
        if self.percorso_immagine:
            self.image = Image(source=self.percorso_immagine, size_hint=(None, None), allow_stretch=True)
            self.image.size = self.image.texture_size  # Imposta la dimensione dell'immagine alle sue dimensioni naturali
            self.image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centra l'immagine nella finestra
            self.add_widget(self.image)
            self.image.bind(on_touch_down=self.on_image_click)

    def on_image_click(self, instance, touch):
        """Gestisce il clic sull'immagine e apre il popup per l'annotazione."""
        if instance.collide_point(touch.x, touch.y):
            # Calcola le coordinate relative
            img_width, img_height = instance.size
            rel_x = touch.x / img_width
            rel_y = touch.y / img_height  # Inverti Y per partire dal basso
            
            # Crea il popup
            self.open_popup(rel_x, rel_y)

    def on_leave(self):
        """Rimuove l'immagine corrente quando si lascia la schermata."""
        if self.image:
            self.remove_widget(self.image)
            self.image = None  # Ripulisce il riferimento all'immagine

    def open_popup(self, rel_x, rel_y):
        """Apre il popup per inserire un'annotazione."""
        content = GridLayout(cols=2)

        content.add_widget(Label(text="Titolo (JSON):"))
        titolo_input = TextInput(multiline=False)
        content.add_widget(titolo_input)

        content.add_widget(Label(text="Testo (JSON):"))
        testo_input = TextInput(multiline=False)
        content.add_widget(testo_input)

        content.add_widget(Label(text="Coordinate X:"))
        coordinate_x_input = TextInput(text=str(rel_x), multiline=False)
        content.add_widget(coordinate_x_input)

        content.add_widget(Label(text="Coordinate Y:"))
        coordinate_y_input = TextInput(text=str(rel_y), multiline=False)
        content.add_widget(coordinate_y_input)

        # Funzione per salvare i dati nel DB
        def save_data(instance):
            titolo = titolo_input.text
            testo = testo_input.text
            coordinata_x = float(coordinate_x_input.text)
            coordinata_y = float(coordinate_y_input.text)
            
            # Usa opera_id e immagine_id per salvare l'annotazione
            if self.opera_id and self.immagine_id:
                db_instance.insert_annotation(self.opera_id, self.immagine_id, titolo, testo, coordinata_x, coordinata_y)
            popup.dismiss()  # Chiudi il popup

        # Aggiungi il pulsante di salvataggio
        save_button = Button(text="Salva")
        save_button.bind(on_press=save_data)
        content.add_widget(save_button)

        # Crea il popup
        popup = Popup(title="Aggiungi Annotazione", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def on_stop(self):
        """Chiude la connessione al database quando l'app viene chiusa."""
        db_instance.close()

