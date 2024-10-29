from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder  
from views.welcome_view import WelcomeScreen
from views.gallery_view import GalleryScreen
from views.opera_view import OperaScreen
from views.info_opera_view import InfoOperaScreen

class MyApp(App):

    def build(self):
        # Carica i file KV per ciascuna schermata
        Builder.load_file('views/welcome_screen.kv')
        Builder.load_file('views/gallery_screen.kv')
        Builder.load_file('views/opera_screen.kv')
        Builder.load_file('views/info_opera_screen.kv')

        # Crea lo ScreenManager
        sm = ScreenManager()

        # Aggiungi tutte le schermate al manager
        sm.add_widget(WelcomeScreen(name='benvenuto'))
        sm.add_widget(GalleryScreen(name='galleria'))
        sm.add_widget(OperaScreen(name='opera'))
        sm.add_widget(InfoOperaScreen(name='info_opera'))
        

        return sm

if __name__ == '__main__':
    MyApp().run()
    
