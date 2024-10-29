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
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from kivy.uix.widget import Widget


class HeaderWidget(BoxLayout):
    logo_source = StringProperty('utils/IMG_Test3.png')

    def __init__(self, **kwargs):
        super(HeaderWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Sezione logo (30%)
        logo_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])
        self.logo_image = Image(source=self.logo_source, allow_stretch=True, keep_ratio=True)
        logo_layout.add_widget(self.logo_image)
        logo_layout.add_widget(BoxLayout(size_hint_x=1))  # Spacer
        self.add_widget(logo_layout)

        # Sezione centrale (40%)
        self.central_layout = BoxLayout(size_hint_x=0.4)
        self.add_widget(self.central_layout)

        # Sezione scelta lingua (30%)
        language_layout = BoxLayout(size_hint_x=0.3, orientation='horizontal', padding=[20, 20, 20, 20])
        language_layout.add_widget(BoxLayout(size_hint_x=1))  # Spacer
        self.language_spinner = Spinner(
            text='IT',
            values=['IT', 'EN', 'FR', 'DE'],
            size_hint_x=None,
            width=100,
            font_size=20,
            color=[1, 1, 1, 1],
            background_color=[0.447, 0.106, 0.157, 1],
            background_normal='',
            background_down=''
        )
        language_layout.add_widget(self.language_spinner)
        self.add_widget(language_layout)

    def update_logo(self, new_logo_path):
        self.logo_source = new_logo_path
        self.logo_image.source = self.logo_source
        self.logo_image.reload()

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

class Card(ButtonBehavior, BoxLayout):
    description = StringProperty('')
    font_size = NumericProperty(36)

    def __init__(self, image_source, description, gallery_screen, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.description = description
        self.gallery_screen = gallery_screen  # Salva il riferimento a GalleryScreen
        self.image_source = image_source  # Salva anche il percorso dell'immagine

        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 5

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=True, size_hint_y=0.8)
        self.label = Label(
            text=self.description,
            font_size=self.font_size,
            padding=[20, 20],
            halign='left',
            valign='top',
            size_hint_y=0.2,
            text_size=(self.width, None),
            color=[0, 0, 0, 1],
            shorten=True,
            shorten_from='right'
        )

        self.add_widget(self.image)
        self.add_widget(self.label)

        self.bind(on_touch_down=self.on_card_click)
        self.bind(size=self._update_rect)
        self.bind(pos=self._update_rect)

        Window.bind(mouse_pos=self.on_card_hover)

    def on_card_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            # Imposta l'immagine da visualizzare nell'OperaScreen
            self.gallery_screen.manager.get_screen('opera').image_source = self.image_source
            App.get_running_app().root.current = 'opera'  # Cambia a OperaScreen

    def on_card_hover(self, instance, touch):
        if self.collide_point(*Window.mouse_pos):
            footer = self.gallery_screen.ids.footer
            if footer:
                footer.update_text(self.description)

    def _update_rect(self, instance, value):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.label.text_size = (self.width, None)


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)

class GalleryScreen(Screen):
    card_data = ListProperty([
        {'image_source': 'utils/IMG_Test.jpg', 'description': "La Cappella dei Magi è un piccolo ambiente posto nel cuore del palazzo, al primo piano. Progettato da Michelozzo, è costituito da un’aula quadrata e da una scarsella sopraelevata per l’altare. L’accesso avveniva da due ingressi: uno privato, per la famiglia, e uno pubblico per accogliere gli ospiti. Il soffitto ligneo, opera di Pagno di Lapo, è finemente intagliato e dorato e sembra specchiarsi, per impianto e forme, sul pregiato pavimento in marmi policromi commessi. Gli affreschi sulle pareti furono realizzati da Benozzo Gozzoli dal 1459 e rappresentano il viaggio dei Magi verso Gesù bambino, raffigurato nella pala d’altare eseguita dalla bottega di Filippo Lippi. Partendo dalla parete est, il corteo avanza con Gaspare (in bianco), poi con Baldassarre (in verde) sulla parete sud, infine con Melchiorre (in rosso) sulla parete ovest. Alla straordinaria ricchezza dei dettagli e degli ornamenti si accompagna l’accurata raffigurazione del paesaggio e di personaggi del tempo posti entro il corteo sacro: fra questi spiccano Cosimo e Piero de’ Medici, i giovani Lorenzo e Giuliano, Gian Galeazzo Sforza e Sigismondo Pandolfo Malatesta, papa Pio II Piccolomini."},
        {'image_source': 'utils/IMG_Test4.jpg', 'description': "Tra le opere esposte a Palazzo Medici Riccardi una delle più celebri è la Madonna con il Bambino, realizzata intorno agli anni Sessanta del Quattrocento da Filippo Lippi. Dopo averne perso a lungo le tracce, il dipinto venne ritrovato nel 1907 presso l’Ospedale di San Salvi a Firenze e  qui trasferito l’anno successivo, ipotizzandone la committenza medicea: questa supposizione fu in parte confermata dal fatto che l’opera proveniva da Castel Pulci, residenza di proprietà dei Riccardi e a loro volta acquirenti del palazzo mediceo. Il dipinto, raffigurante la Madonna che si accosta dolcemente alla guancia del Bambino, riprende una composizione tipica del Rinascimento fiorentino, che il Lippi rappresenta con grazia e naturalezza. L’opera fu molto ammirata e copiata proprio per i suoi preziosi effetti di luce e per l’eleganza delle linee di contorno. È osservabile anche il retro della tavola, che mostra un disegno preparatorio di testa maschile."},
        {'image_source': 'utils/IMG_Test5.jpg', 'description': "La Galleria del palazzo e l’attigua Biblioteca furono edificate tra il 1670 e il 1677 per volontà della famiglia Riccardi; a sovrintendere i lavori fu inizialmente l’architetto Pier Maria Baldi, sostituito poi da Giovan Battista Foggini. La decorazione della volta della Galleria iniziò solo nell’estate del 1682, quando Luca Giordano accolse la proposta del marchese Francesco Riccardi, per concludersi nel 1685. Il ricco e colto programma iconografico, concepito senza soluzione di continuità sull’intera superficie voltata, è declinato con un vastissimo numero di figure e una cromia chiara e luminosa."},
        {'image_source': 'utils/IMG_Test6.jpg', 'description': "Il Museo dei Marmi espone una selezione di opere scultoree provenienti dalle collezioni antiquarie della famiglia Riccardi, appassionati collezionisti di marmi antichi, qui trasferite dalla precedente villa di Gualfonda. Quando il palazzo, nel 1810, venne alienato al demanio, solo una parte della collezione Riccardi fu trasferita nelle collezioni pubbliche, mentre il resto rimase all’interno dell’edificio ed è oggi visibile tra il Museo dei Marmi e il percorso di visita al primo piano. Si tratta soprattutto di busti marmorei di età romana raffiguranti saggi, eroi, imperatori o dei: fra questi l’imperatore Caracalla, Vibia Sabina, Euripide, Anacreonte, Sofocle e il superbo busto di atleta. Vi sono anche i calchi in gesso dei busti di Augusto e di Agrippa, i cui originali furono donati da papa Sisto IV a Lorenzo il Magnifico nel 1471, e quelli di Caligola e Nerone, acquistati dai Riccardi nel 1669; tutti gli originali sono conservati alle Gallerie degli Uffizi."},
    ])

    visible_cards = 3
    current_index = 0

    def __init__(self, **kwargs):
        super(GalleryScreen, self).__init__(**kwargs)
        self.update_cards()

    def update_cards(self):
        self.ids.card_grid.clear_widgets()
        end_index = self.current_index + self.visible_cards
        cards_to_display = self.card_data[self.current_index:end_index]

        for data in cards_to_display:
            card = Card(image_source=data['image_source'], description=data['description'], gallery_screen=self)
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
