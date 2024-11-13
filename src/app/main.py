from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from views.welcome_view import WelcomeScreen
from views.gallery_view import GalleryScreen
from views.opera_view import OperaScreen
from views.info_opera_view import InfoOperaScreen
from views.login_view import LoginScreen  
from views.registration_view import RegistrationScreen  
from views.add_operas_view import AddOperasScreen
from views.add_details_view import AddDetailsScreen
from kivy.core.window import Window

class MuseumApp(App):

    def build(self):
        # Window.fullscreen = True

        # Carica i file KV per ciascuna schermata
        Builder.load_file('views/welcome_screen.kv')
        Builder.load_file('views/gallery_screen.kv')
        Builder.load_file('views/opera_screen.kv')
        Builder.load_file('views/info_opera_screen.kv')
        Builder.load_file('views/login_screen.kv') 
        Builder.load_file('views/registration_screen.kv')  
        Builder.load_file('views/add_operas_screen.kv')   
        Builder.load_file('views/add_details_screen.kv')  
        # Crea lo ScreenManager
        sm = ScreenManager()

        # Aggiungi tutte le schermate al manager
        sm.add_widget(WelcomeScreen(name='benvenuto'))
        sm.add_widget(GalleryScreen(name='galleria'))
        sm.add_widget(OperaScreen(name='opera'))
        sm.add_widget(InfoOperaScreen(name='info_opera'))
        sm.add_widget(LoginScreen(name='login'))  
        sm.add_widget(RegistrationScreen(name='registrazione'))  
        sm.add_widget(AddOperasScreen(name='aggiungi_opere'))  
        sm.add_widget(AddDetailsScreen(name='aggiungi_dettagli'))  

        return sm

if __name__ == '__main__':
    MuseumApp().run()
