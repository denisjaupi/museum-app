from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.button import Button




class Card(ButtonBehavior, BoxLayout):
    """ Classe per le card, estende ButtonBehavior per renderle cliccabili. """
    description = StringProperty('')

    def __init__(self, image_source, description, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.description = description

        # Imposta l'orientamento della Card e il padding
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 5  # Aggiungi un po' di spazio tra immagine e label

        # Sfondo grigio chiaro per la card
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Colore di sfondo grigio chiaro
            self.rect = Rectangle(pos=self.pos, size=self.size)  # Inizializza il rettangolo

        # Immagine che occupa il 60% dello spazio
        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=True, size_hint_y=0.6)

        # Label che occupa il 40% dello spazio
        self.label = Label(
            text=self.description,
            font_size=36,
            halign='left',
            valign='top',
            size_hint_y=0.4,  # Occupare il 40% dell'altezza
            text_size=(self.width, None),  # Permette di andare a capo
            color=[0, 0, 0, 1],  # Testo nero
            shorten=True,  # Abilita il troncamento
            shorten_from='right'  # Troncamento dal lato destro
        )

        # Aggiungi immagine e label alla card
        self.add_widget(self.image)
        self.add_widget(self.label)

        # Rendi la card cliccabile
        self.bind(on_touch_down=self.on_card_click)
        self.bind(size=self._update_rect)  # Aggiorna il rettangolo quando la dimensione cambia
        self.bind(pos=self._update_rect)  # Aggiorna il rettangolo quando la posizione cambia

        Window.bind(mouse_pos=self.on_card_hover)  # Controlla l'hover del mouse

    def on_card_click(self, instance, touch):
        """ Gestisce il clic sulla card. """
        if self.collide_point(*touch.pos):
            App.get_running_app().root.current = 'opera'
            print(f'Card clicked: {self.description}')

    def on_card_hover(self, instance, touch):
        """ Gestisce l'hover della card. """
        if self.collide_point(*touch):
            print(f'Card hovered: {self.description}')

    def _update_rect(self, instance, value):
        """ Aggiorna la posizione e le dimensioni del rettangolo di sfondo. """
        if hasattr(self, 'rect'):  # Controlla se l'attributo rect esiste
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)  # Aggiorna il text_size della label


class GalleryScreen(Screen):
    # Lista delle opere (ognuna rappresentata da un dizionario con immagine e descrizione)
    card_data = ListProperty([
        {'image_source': 'IMG_Test.jpg', 'description': "La Cappella dei Magi, affrescata da Benozzo Gozzoli."},
        {'image_source': 'IMG_Test.jpg', 'description': "La Galleria terrena con sculture e stucchi."},
        {'image_source': 'IMG_Test.jpg', 'description': "Gli scavi archeologici restituiscono storia."},
        {'image_source': 'IMG_Test.jpg', 'description': "Una vista panoramica delle collezioni storiche."},

    ])

    visible_cards = 3
    current_index = 0

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)
        self.update_cards()

    def update_cards(self):
        # Svuota la griglia prima di riempirla di nuovo
        self.ids.card_grid.clear_widgets()

        # Calcola l'indice finale e seleziona le opere da visualizzare
        end_index = self.current_index + self.visible_cards
        cards_to_display = self.card_data[self.current_index:end_index]

        # Aggiungi le card alla griglia
        for data in cards_to_display:
            card = Card(image_source=data['image_source'], description=data['description'])
            self.ids.card_grid.add_widget(card)

        # Aggiungi spazi vuoti per riempire i posti mancanti, se meno di 3 card
        empty_slots = self.visible_cards - len(cards_to_display)
        for _ in range(empty_slots):
            self.ids.card_grid.add_widget(Widget())  # Widget vuoto per riempire gli spazi mancanti

    def scroll_left(self):
        if self.current_index > 0:
            # Diminuisce di 3 l'indice corrente per visualizzare il gruppo precedente
            self.current_index -= self.visible_cards
            self.update_cards()

    def scroll_right(self):
        # Incrementa di 3 l'indice corrente per visualizzare il prossimo gruppo
        if self.current_index + self.visible_cards < len(self.card_data):
            self.current_index += self.visible_cards
            self.update_cards()



class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class MyApp(App):
    def build(self):
        return GalleryScreen()

if __name__ == '__main__':
    MyApp().run()
