from kivy.uix.screenmanager import Screen

class LoginScreen(Screen):
    def login_user(self):
        username = self.ids.username.text
        password = self.ids.password.text
        # Logica di autenticazione da aggiungere
        print(f"Attempting login with Username: {username}, Password: {password}")
