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
from models import db, User , Personajes , Planetas, Usuarios, Favoritos
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planets():

    response_body = Planetas.query.all()
    if response_body==[]:
        return jsonify({"msg":"No existe ningun planeta"}), 404
    result= list(map(lambda planeta:planeta.serialize(),response_body))
    return jsonify(result), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_by_id(id):

    response_body = Planetas.query.filter_by(id=id).first()
    if response_body is None:
        return jsonify({"msg":"No existe ningun planeta"}), 404
    return jsonify(response_body.serialize()), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():

    response_body = Personajes.query.all()
    if response_body==[]:
        return jsonify({"msg":"No existe ningun personaje"}), 404
    result= list(map(lambda personajes:personajes.serialize(),response_body))
    return jsonify(result), 200

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personajes_by_id(id):

    response_body = Personajes.query.filter_by(id=id).first()
    if response_body is None:
        return jsonify({"msg":"No existe ningun personaje"}), 404
    return jsonify(response_body.serialize()), 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():

    response_body = Usuarios.query.all()
    if response_body==[]:
        return jsonify({"msg":"No existe ningun usuario"}), 404
    result= list(map(lambda usuarios:usuarios.serialize(),response_body))
    return jsonify(result), 200


@app.route('/usuarios/favorites/<int:user_id>', methods=['GET'])
def get_usuarios_favoritos(user_id):

    response_body = Favoritos.query.filter_by(user_id=user_id).all()
    if response_body==[]:
        return jsonify({"msg":"No existe ningun favorito para este usuario"}), 404
    result= list(map(lambda usuarios:usuarios.serialize(),response_body))
    return jsonify(result), 200
    

@app.route('/favorite/planet/<int:planet_id>', methods=['POST',"DELETE"])
def post_planetas_favoritos(planet_id):
    
    body = request.json
    email = body.get("email")
    user = Usuarios.query.filter_by(mail=email).first()
    if user is None:
        return jsonify({"msg":"No existe ningun usuario"}), 404
    planeta = Planetas.query.filter_by(id=planet_id).first()
    if planeta is None:
        return jsonify({"msg":"No existe ningun planeta"}), 404
    
    if request.method=="POST":
        new_favorite = Favoritos(
            user_id=user.id,
            planetas_id=planet_id
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    if request.method=="DELETE":
        favorite_delete = Favoritos.query.filter_by(user_id=user.id,planetas_id=planet_id).first()
        if favorite_delete is None:
            return jsonify({"msg":"no existe el favorito"}), 404
        db.session.delete(favorite_delete)
        db.session.commit()
        return jsonify({"msg":"favorito eliminado"}), 200
    
@app.route('/favorite/personajes/<int:personajes_id>', methods=['POST',"DELETE"])
def post_personajes_favoritos(personajes_id):
    
    body = request.json
    email = body.get("email")
    user = Usuarios.query.filter_by(mail=email).first()
    if user is None:
        return jsonify({"msg":"No existe ningun usuario"}), 404
    personaje = Personajes.query.filter_by(id=personajes_id).first()
    if personaje is None:
        return jsonify({"msg":"No existe ningun personaje"}), 404
    
    if request.method=="POST":  
        new_favorite = Favoritos(
            user_id=user.id,
            personajes_id=personajes_id
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201   
    
    if request.method=="DELETE":
        favorite_delete = Favoritos.query.filter_by(user_id=user.id,personajes_id=personajes_id).first()
        if favorite_delete is None:
            return jsonify({"msg":"no existe el favorito"}), 404
        db.session.delete(favorite_delete)
        db.session.commit()
        return jsonify({"msg":"favorito eliminado"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

