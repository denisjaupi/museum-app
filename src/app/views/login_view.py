from kivy.uix.screenmanager import Screen
from database.db_connection import DBConnection
import bcrypt

class LoginScreen(Screen):

    def login_user(self):
        username = self.ids.username.text
        password = self.ids.password.text

        # Reset degli errori prima di effettuare una nuova prova
        self.ids.username_error.opacity = 0
        self.ids.password_error.opacity = 0

        # Crea una connessione al database
        db = DBConnection(host="localhost", port="5432", database="museum_db", user="postgres", password="postgres")
        db.connect()  

        # Recupera l'hash della password dal database per il nome utente
        stored_password_hash = db.get_password_hash(username)

        if stored_password_hash:
            # Confronta la password inserita con l'hash memorizzato
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print("Login riuscito!")
                self.reset_form()
                self.manager.current = 'aggiungi_opere'  # Vai alla schermata di aggiunta delle opere
            else:
                print("Password errata!")
                self.ids.password_error.text = "Password errata!"
                self.ids.password_error.opacity = 1  # Mostra l'errore per la password
        else:
            print("Nome utente non trovato!")
            self.ids.username_error.text = "Nome utente non trovato!"
            self.ids.username_error.opacity = 1  # Mostra l'errore per il nome utente

        db.close()

    def reset_form(self):
        """Reset dei campi di input dopo la registrazione."""
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.username_error.text = ""
        self.ids.username_error.opacity = 0
        self.ids.password_error.text = ""  
        self.ids.password_error.opacity = 0  
