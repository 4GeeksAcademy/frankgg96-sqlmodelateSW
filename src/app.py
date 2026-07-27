"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = db.session.execute(db.select(Character)).scalars().all()
    people_list = [ppl.serialize() for ppl in people]
    return jsonify(people_list)


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = db.session.execute(db.select(Character).filter_by(id=people_id)).scalar_one_or_none()
    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200



@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets():
    planets = db.session.execute(db.selec(Planet)).scalars().all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = db.session.execute(db.select(Planet).filter_by(id=planet_id)).scalar_one_or_none()
    if planet is None:
        return jsonify({"Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200


           
@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200

@app.route('/users/favorites', methods=['GET'])
def guet_user_favorites():
    current_user_id = 1
    favorites = db.session.execute(db.select(Favorite).filter_by(users_id=current_user_id)).scalars().all()
    favorites_list = [fav.serialize() for fav in favorites]
    return jsonify(favorites_list), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1   
    planet = db.session.execute(db.select(Planet).filter_by(id=planet_id)).scalar_one_or_none()
    if planet is None:
        return jsonify({"msg": "El planeta no existe"}), 404 
    existing_fav = db.session.execute(db.select(Favorite).filter_by(user_id=current_user_id, planet_id=planet_id)).scalar_one_or_none()
    if existing_fav:
        return jsonify({"msg": "Este planeta ya está en tus favoritos"}), 400

    new_fav = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_fav) 
    db.session.commit() 
    return jsonify({"msg": "Planeta agregado a favoritos"}), 201





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
