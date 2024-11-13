# add_operas_view.py
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from database.db_connection import DBConnection

class OperaCard(ButtonBehavior, BoxLayout):
    """Custom widget for displaying an opera card with an image as the background."""
    def __init__(self, opera, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (200, 200)

        # Imposta l'immagine di sfondo della card
        if opera['immagine_principale']:
            image = Image(source=opera['immagine_principale'], allow_stretch=True, keep_ratio=False)
            self.add_widget(image)
        
        # Aggiungi un’etichetta per il titolo
        label = Label(text=opera['title'], size_hint_y=None, height=30, color=[0.9, 0.9, 0.9, 1])
        self.add_widget(label)

class AddOperasScreen(Screen):
    footer = ObjectProperty(None)
    operas = ListProperty([])  
    items_per_page = 3  
    current_offset = 0

    def on_logo_click(self):
        popup = Popup(
            title="Seleziona un nuovo simbolo per il logo",
            content=Label(text="Sostituisci il simbolo o icona del logo qui"),
            size_hint=(0.5, 0.5)
        )
        popup.open()

    def on_enter(self):
        self.load_operas_from_db()

    def load_operas_from_db(self):
        """Carica le opere dal database e aggiorna self.operas."""
        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()

        query = "SELECT id, titolo, autore, descrizione, immagine_principale FROM opere_d_arte"
        results = db.execute_query(query)

        self.operas = [
            {
                'id': row[0],
                'title': row[1].get('it', 'Senza titolo'),  # Assicurati di gestire JSON correttamente
                'author': row[2],
                'description': row[3].get('it', ''),
                'immagine_principale': row[4]
            }
            for row in results
        ]

        db.close()
        self.update_grid()

    def add_opera_card(self):
        self.open_opera_details()


    def update_grid(self):
        # Pulisce la griglia per mostrare solo le nuove card
        self.ids.card_grid.clear_widgets()

        # Calcola l'intervallo dell'attuale pagina di opere
        start_index = self.current_offset
        end_index = start_index + self.items_per_page
        operas_to_display = self.operas[start_index:end_index]

        # Calcola il numero di colonne per la griglia
        columns = 3

        # Aggiunge le opere correnti alla griglia
        for i, opera in enumerate(operas_to_display):
            card = OperaCard(opera)
            card.size_hint = (None, None)  # Rimuove la larghezza dinamica per evitare che si espanda
            card.width = self.ids.card_grid.width / columns  # Assegna un terzo della larghezza alla card
            card.bind(on_release=lambda instance, opera=opera: self.open_opera_details(opera))
            self.ids.card_grid.add_widget(card)


    def scroll_right(self):
        # Scorri in avanti di 3 opere se possibile
        if self.current_offset + self.items_per_page < len(self.operas):
            self.current_offset += self.items_per_page
            self.update_grid()

    def scroll_left(self):
        # Scorri indietro di 3 opere se possibile
        if self.current_offset - self.items_per_page >= 0:
            self.current_offset -= self.items_per_page
            self.update_grid()

    def open_opera_details(self, opera=None):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        image_selection = FileChooserIconView(size_hint=(1, 0.6))
        layout.add_widget(image_selection)

        title_author_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        title_input = TextInput(text=opera['title'] if opera else '', hint_text="Titolo", multiline=False, size_hint_x=0.5)
        author_input = TextInput(text=opera['author'] if opera else '', hint_text="Autore", multiline=False, size_hint_x=0.5)
        title_author_layout.add_widget(title_input)
        title_author_layout.add_widget(author_input)
        layout.add_widget(title_author_layout)

        description_input = TextInput(text=opera['description'] if opera else '', hint_text="Descrizione", multiline=True, size_hint_y=None, height=150)
        layout.add_widget(description_input)

        submit_button = Button(text="Salva", size_hint_y=None, height=50)
        submit_button.bind(on_release=lambda x: self.save_opera_details(
            title=title_input.text,
            author=author_input.text,
            description=description_input.text,
            image_paths=image_selection.selection,
            opera_id=opera['id'] if opera else None
        ))
        layout.add_widget(submit_button)

        self.popup = Popup(title="Aggiungi Dettagli Opera", content=layout, size_hint=(0.8, 0.9))
        self.popup.open()

    def save_opera_details(self, title, author, description, image_paths, opera_id=None):
        if title and author and description:
            db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
            db.connect()

            main_image = image_paths[0] if image_paths else None
            if opera_id:
                # Logica per aggiornare un'opera esistente
                query = """
                UPDATE opere_d_arte SET titolo = %s, autore = %s, descrizione = %s, immagine_principale = %s
                WHERE id = %s
                """
                params = (json.dumps({"it": title, "en": title}), author, json.dumps({"it": description, "en": description}), main_image, opera_id)
            else:
                db.insert_opera(
                    titolo={"it": title, "en": title},
                    autore=author,
                    descrizione={"it": description, "en": description},
                    immagine_principale=main_image
                )

            db.close()
            self.load_operas_from_db()
            self.popup.dismiss()

            print(f"Opera aggiunta: Titolo={title}, Autore={author}, Descrizione={description}, Immagine Principale={main_image}")
        else:
            print("Tutti i campi sono obbligatori!")