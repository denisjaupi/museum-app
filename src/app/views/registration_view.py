from kivy.uix.screenmanager import Screen

class RegistrationScreen(Screen):
    def register_user(self):
        username = self.ids.username.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        if password == confirm_password:
            # Logica di registrazione da aggiungere
            print(f"Registering new user with Username: {username}")
        else:
            print("Le password non coincidono!")
