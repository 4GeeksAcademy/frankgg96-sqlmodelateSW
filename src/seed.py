import os
from flask import Flask
# Importa tu instancia de base de datos y modelos aquí
# Cambia 'models' por el nombre del archivo donde tienes tus clases
from models import db, User, Planet, Character, Favorite

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos proporcionada
    db_url = os.getenv("DATABASE_URL")
    if db_url is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    
    # Desactivar el trackeo de modificaciones para evitar advertencias
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Borrando tablas existentes...")
        db.drop_all()
        
        print("Creando tablas...")
        db.create_all()
        
        print("Poblando Planetas...")
        planets = [
            Planet(name="Tatooine", climate="Arid", population=200000),
            Planet(name="Alderaan", climate="Temperate", population=2000000000),
            Planet(name="Hoth", climate="Frozen", population=0)
        ]
        db.session.add_all(planets)
        
        print("Poblando Personajes...")
        characters = [
            Character(name="Luke Skywalker", gender="Male", eye_color="Blue"),
            Character(name="Leia Organa", gender="Female", eye_color="Brown"),
            Character(name="Darth Vader", gender="Male", eye_color="Yellow")
        ]
        db.session.add_all(characters)
        
        print("Poblando Usuarios...")
        users = [
            User(first_name="Juan", last_name="Pérez", email="juan@example.com", password="hashed_password_1", subscription_date="2023-10-01"),
            User(first_name="Maria", last_name="Gómez", email="maria@example.com", password="hashed_password_2", subscription_date="2023-11-15")
        ]
        db.session.add_all(users)
        
        # Guardamos los cambios para que se generen los IDs en la base de datos
        db.session.commit()
        print("¡Planetas, Personajes y Usuarios creados!")

        print("Poblando Favoritos...")
        # Usamos los objetos ya creados (que ahora tienen un .id asignado) para crear las relaciones
        favorites = [
            Favorite(user_id=users[0].id, planet_id=planets[0].id), # A Juan le gusta Tatooine
            Favorite(user_id=users[0].id, character_id=characters[0].id), # A Juan le gusta Luke
            Favorite(user_id=users[1].id, character_id=characters[1].id), # A Maria le gusta Leia
            Favorite(user_id=users[1].id, planet_id=planets[1].id) # A Maria le gusta Alderaan
        ]
        db.session.add_all(favorites)
        db.session.commit()
        
        print("¡Base de datos poblada exitosamente!")

if __name__ == "__main__":
    seed_database()