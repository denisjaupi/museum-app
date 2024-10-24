from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder  
from views.welcome_view import WelcomeScreen
from views.gallery_view import GalleryScreen
from views.opera_view import OperaScreen
from views.info_opera_view import InfoOperaScreen

class MyApp(App):

    def build(self):
        # Carica il file KV manualmente
        Builder.load_file('museum-app.kv')

        # Creiamo lo ScreenManager
        sm = ScreenManager()

        # Aggiungiamo tutte le schermate al manager
        sm.add_widget(WelcomeScreen(name='benvenuto'))
        sm.add_widget(GalleryScreen(name='galleria'))
        sm.add_widget(OperaScreen(name='opera'))
        sm.add_widget(InfoOperaScreen(name='info_opera'))

        return sm

if __name__ == '__main__':
    MyApp().run()
