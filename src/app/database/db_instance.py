from app.database import db_connection as db
from config import DB_CONFIG 

# Crea un'istanza globale del database
db_instance = db.DBConnection(
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"]
)

# Connetti subito al database
db_instance.connect()
