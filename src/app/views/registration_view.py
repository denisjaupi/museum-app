from kivy.uix.screenmanager import Screen
from database.db_connection import DBConnection
import bcrypt

class RegistrationScreen(Screen):

    def register_user(self):
        username = self.ids.username.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        
        # Verifica se le password corrispondono
        if password == confirm_password:
            # Connessione al database
            db = DBConnection(host="localhost", port="5432", database="museum_app_db", user="postgres", password="postgres")
            db.connect()         
            # Controlla se l'utente esiste già
            existing_user = db.get_user_by_username(username)
            if existing_user:
                print("Nome utente già esistente!")
                return
            
            # Hash della password
            password_hash = self.hash_password(password)

            # Inserisci il nuovo utente nel database
            try:
                db.insert_user(username, password_hash)
                print(f"Utente {username} registrato con successo!")
                self.reset_form()  # Reset the form and go back to login
                self.manager.current = 'login'  # Cambia schermata al login
            except Exception as e:
                print(f"Errore durante la registrazione: {e}")
        else:
            print("Le password non coincidono!")
            self.show_password_error()  # Mostra l'errore nella UI

    def hash_password(self, password: str) -> str:
        """
        Crea un hash sicuro della password usando bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def show_password_error(self):
        """Mostra un errore se le password non coincidono."""
        self.ids.password_error.text = "Le password non coincidono!"  # Mostra l'errore
        self.ids.password_error.opacity = 1  # Rende visibile l'errore

    def reset_form(self):
        """Reset dei campi di input dopo la registrazione."""
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.confirm_password.text = ""
        self.ids.password_error.text = ""  # Pulisce l'errore
        self.ids.password_error.opacity = 0  # Nasconde l'errore
