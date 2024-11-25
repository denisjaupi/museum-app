from app.database.db_instance import db_instance

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView


class Card(ButtonBehavior, BoxLayout):
    title = StringProperty('')  # Titolo dell'opera
    description = StringProperty('')  # Descrizione dell'opera
    image_source = StringProperty('')  # Percorso dell'immagine
    opera_id = NumericProperty(0)  # ID dell'opera, deve essere un numero (int o float)

    def __init__(self, title, description, image_source, opera_id, add_operas_screen, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.add_operas_screen = add_operas_screen
        self.title = title
        self.description = description
        self.image_source = image_source
        self.opera_id = opera_id

        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 5

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Carica l'immagine dal path
        self.image = Image(source=self.image_source, allow_stretch=True, keep_ratio=True, size_hint_y=0.8)

        # Aggiorna il Label per mostrare il titolo invece della descrizione
        self.label = Label(
            text=self.title,  # Cambiato a self.title per mostrare il titolo
            font_name='src/app/utils/Montserrat-Bold.ttf',
            halign='center',
            valign='top',
            size_hint_y=0.2,
            text_size=(self.width, None),
            color=[0, 0, 0, 1],
            shorten=True,
            shorten_from='right'
        )

        self.add_widget(self.image)
        self.add_widget(self.label)

        # Lega il comportamento di clic e dimensione
        self.bind(on_touch_down=self.on_card_click)
        self.bind(size=self._update_rect)
        self.bind(pos=self._update_rect)

    def on_card_click(self, instance, touch):
        """Quando si clicca sulla card, si va alla pagina dell'opera con il popup."""
        if self.collide_point(*touch.pos):
            # Crea il layout per il popup
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

            query_details = f"""
                SELECT titolo->'{self.add_operas_screen.current_language}', descrizione->'{self.add_operas_screen.current_language}', autore, percorso_immagine
                FROM opere_d_arte
                WHERE id = {self.opera_id};
            """
            result = db_instance.execute_query(query_details)
            db_instance.close()

            if result:
                title, description, author, image_path = result[0]

                # Layout orizzontale per le immagini
                images_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=200, spacing=10)

                # Recupera le immagini associate a questa opera (con immagine_id e percorso_immagine)
                db_instance.connect()
                query_images = f"""
                    SELECT immagine_id, percorso_immagine
                    FROM opere_d_arte 
                    WHERE id = {self.opera_id};
                """
                images = db_instance.execute_query(query_images)
                db_instance.close()

                # Usa un GridLayout per i pulsanti in modo che si distribuiscano orizzontalmente
                buttons_layout = GridLayout(cols=len(images), size_hint_y=None, height=40, spacing=10)  
                for image in images:
                    image_id = image[0]  # immagine_id
                    image_button = Button(
                        text=f"Immagine {image_id}",  # Mostra il 'immagine_id' come testo del bottone
                        size_hint_x=1,  # I pulsanti occupano tutto lo spazio orizzontale disponibile
                        on_release=lambda btn, img_id=image_id: self.on_image_button_click(img_id)
                    )
                    buttons_layout.add_widget(image_button)

                    # Aggiungi le immagini al layout
                    opera_image = Image(source=image[1], allow_stretch=True, height=150, width=150)  # usa percorso_immagine per il source
                    images_layout.add_widget(opera_image)

                layout.add_widget(buttons_layout)  # Aggiungi i pulsanti sopra le immagini
                layout.add_widget(images_layout)   # Aggiungi le immagini sotto i pulsanti

                # Layout per Titolo e Autore (affiancati)
                title_author_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
                
                # Etichetta per il titolo
                title_label = Label(text="Titolo", size_hint_x=None, width=80)
                title_author_layout.add_widget(title_label)

                # Campo di input per il titolo
                title_input = TextInput(text=title, hint_text="Modifica il titolo", size_hint_x=1, height=40)
                title_author_layout.add_widget(title_input)

                # Etichetta per l'autore
                author_label = Label(text="Autore", size_hint_x=None, width=80)
                title_author_layout.add_widget(author_label)

                # Campo di input per l'autore
                author_input = TextInput(text=author, hint_text="Autore dell'opera", size_hint_x=1, height=40)
                title_author_layout.add_widget(author_input)

                layout.add_widget(title_author_layout)

                # Etichetta per la descrizione
                description_label = Label(text="Descrizione", size_hint_y=None, height=40)
                layout.add_widget(description_label)

                # Campo di input per la descrizione
                description_input = TextInput(text=description, hint_text="Modifica descrizione", multiline=True, size_hint_y=None, height=150)
                layout.add_widget(description_input)

                # Bottone per salvare le modifiche
                save_button = Button(
                    text="Salva modifiche",
                    size_hint_y=None,
                    height=50
                )
                save_button.bind(on_release=lambda x: self.save_changes(title_input.text, author_input.text, description_input.text, self.popup))
                layout.add_widget(save_button)

                # Bottone per chiudere il popup
                close_button = Button(
                    text="Chiudi",
                    size_hint_y=None,
                    height=50
                )
                close_button.bind(on_release=lambda x: self.popup.dismiss())
                layout.add_widget(close_button)

                # Crea il popup
                self.popup = Popup(
                    title="Dettagli Opera",
                    content=layout,
                    size_hint=(0.8, 0.9)  # Aggiusta la dimensione del popup
                )
                self.popup.open()

    def close_popup(self):
        """Chiude il popup quando si cambia schermata."""
        if self.popup:
            self.popup.dismiss()

    def on_image_button_click(self, image_id):
        """Gestisci il click su uno dei pulsanti delle immagini."""
        print(f"Immagine selezionata: {image_id}")

        # Query per ottenere id, immagine_id e percorso_immagine
        query = f"""
            SELECT id, immagine_id, percorso_immagine
            FROM opere_d_arte
            WHERE immagine_id = {image_id};
        """
        result = db_instance.execute_query(query)
        db_instance.close()

        if result:
            opera_id, immagine_id, percorso_immagine = result[0]
 
            # Passa le informazioni alla schermata "aggiungi_dettagli"
            add_details_screen = self.add_operas_screen.manager.get_screen('aggiungi_dettagli')
            add_details_screen.set_image_data(opera_id, immagine_id, percorso_immagine)

            # Chiudi il popup se è aperto
            self.close_popup()

            App.get_running_app().root.current = 'aggiungi_dettagli'


    def save_changes(self, title, author, description, popup):
        """Salva le modifiche nel database"""

        # Query di aggiornamento
        update_query = f"""
            UPDATE opere_d_arte 
            SET titolo = '{title}', autore = '{author}', descrizione = '{description}'
            WHERE id = {self.opera_id};
        """
        db_instance.execute_query(update_query)
        db_instance.commit()  # Applica le modifiche
        db_instance.close()

        # Chiudi il popup dopo aver salvato le modifiche
        popup.dismiss()

    def _update_rect(self, instance, value):
        """Assicura che la rect e il testo si aggiornino correttamente durante i cambiamenti di dimensione"""
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class AddOperasScreen(Screen):
    card_data = ListProperty([])  # La lista delle opere d'arte verrà aggiornata dinamicamente
    visible_cards = 3
    current_index = 0
    current_language = 'it'  # Lingua predefinita (italiano)

    def __init__(self, **kwargs):
        super(AddOperasScreen, self).__init__(**kwargs)
        self.fetch_opere_d_arte()  # Recupera i dati dal database
        self.update_cards()
            

    def fetch_opere_d_arte(self):
        """Recupera i dati delle opere d'arte dal database e aggiorna card_data."""
        try:
            # Modifica la query per includere solo le opere con id_immagine=1
            query = f"""
                SELECT id, titolo->'{self.current_language}', descrizione->'{self.current_language}', percorso_immagine 
                FROM opere_d_arte 
                WHERE immagine_id = 1;
            """
            results = db_instance.execute_query(query)

            if results:
                # Aggiungi l'ID dell'opera alla card_data
                self.card_data = [
                    {'id': row[0], 'title': row[1], 'description': row[2], 'image_source': row[3]} for row in results
                ]
        finally:
            db_instance.close()  # Chiudi la connessione



    def update_cards(self):
        self.ids.card_grid.clear_widgets()
        end_index = self.current_index + self.visible_cards
        cards_to_display = self.card_data[self.current_index:end_index]

        for data in cards_to_display:
            # Assicurati che title e description siano stringhe
            title = str(data['title']) if not isinstance(data['title'], str) else data['title']
            description = str(data['description']) if not isinstance(data['description'], str) else data['description']
            image_source = data['image_source']  # Il percorso dell'immagine
            opera_id = data.get('id', '') # ID dell'opera

            # Passa il titolo, la descrizione e l'immagine alla Card
            card = Card(title=title, description=description, image_source=image_source, opera_id=opera_id, add_operas_screen=self)
            self.ids.card_grid.add_widget(card)

        empty_slots = self.visible_cards - len(cards_to_display)
        for _ in range(empty_slots):
            self.ids.card_grid.add_widget(Widget())

    def scroll_left(self):
        if self.current_index > 0:
            self.current_index -= self.visible_cards
            self.update_cards()

    def scroll_right(self):
        if self.current_index + self.visible_cards < len(self.card_data):
            self.current_index += self.visible_cards
            self.update_cards()

    def open_add_art_popup(self):
        """Apre il popup per aggiungere opere d'arte."""
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # FileChooser per selezione multipla
        filechooser = FileChooserListView(multiselect=True, filters=['*.png', '*.jpg', '*.jpeg'])
        popup_layout.add_widget(filechooser)

        # Campi di input
        fields = GridLayout(cols=2, size_hint_y=None)
        fields.bind(minimum_height=fields.setter('height'))

        fields.add_widget(Label(text="Titolo (JSON):"))
        titolo_input = TextInput(multiline=False)
        fields.add_widget(titolo_input)

        fields.add_widget(Label(text="Autore:"))
        autore_input = TextInput(multiline=False)
        fields.add_widget(autore_input)

        fields.add_widget(Label(text="Descrizione (JSON):"))
        descrizione_input = TextInput(multiline=True)
        fields.add_widget(descrizione_input)

        fields.add_widget(Label(text="Sottotitolo:"))
        sottotitolo_input = TextInput(multiline=False)
        fields.add_widget(sottotitolo_input)

        popup_layout.add_widget(fields)

        # Pulsanti per azioni
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_button = Button(text="Salva", size_hint_x=0.5)
        close_button = Button(text="Chiudi", size_hint_x=0.5)

        def save_data(instance):
            """Salva i dati nel database."""
            files = filechooser.selection
            titolo = titolo_input.text
            autore = autore_input.text
            descrizione = descrizione_input.text
            sottotitolo = sottotitolo_input.text

            if files and titolo and autore:
                for idx, file_path in enumerate(files):
                    # Utilizza il metodo save_operas per salvare l'opera d'arte nel database
                    self.db.insert_operas(titolo, autore, descrizione, file_path, sottotitolo)

            popup.dismiss()  # Chiude il popup



        save_button.bind(on_press=save_data)
        close_button.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(save_button)
        button_layout.add_widget(close_button)
        popup_layout.add_widget(button_layout)

        # Creazione e apertura del popup
        popup = Popup(title="Aggiungi Opere d'Arte", content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def on_stop(self):
        """Chiude la connessione al database quando l'app viene chiusa."""
        self.db.close()