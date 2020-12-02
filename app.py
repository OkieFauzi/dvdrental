from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw' : 'parallelepiped',
    'db' : 'dvdrental',
    'host' : 'localhost',
    'port' : '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)
ma = Marshmallow(app)
from models import Actor, ActorSchema, Film, FilmSchema, Country, CountrySchema

#global variable
actors_schema = ActorSchema(many=True)
actor_schema = ActorSchema()
film_schema = FilmSchema()
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)

@app.route('/index', methods = ['GET'])
def index():
    return 'Hello World'

@app.route('/actor', methods = ['GET'])
def get_actors():
    try:
        actors = Actor.query.all()
        return jsonify(data=actors_schema.dump(actors))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/actor/<_id>', methods = ['GET'])
def get_actors_by_id(_id):
    try:
        actor = Actor.query.filter_by(actor_id = _id).first()
        return jsonify(actor_schema.dump(actor))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/actor/<_id>', methods = ['PUT'])
def update_actor(_id):
    body = request.json
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    try:
        actor = Actor.query.filter_by(actor_id=_id).first()
        actor.first_name = first_name
        actor.last_name = last_name
        db.session.commit()
        return jsonify(actor_schema.dump(actor))
    except Exception as e:
        return jsonify(error=str(e))  

@app.route('/actor/add', methods = ['POST'])
def actor_add():
    body = request.json
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    try:
        actor = Actor(first_name, last_name)
        db.session.add(actor)
        db.session.commit()
        return jsonify(actor_schema.dump(actor))
    except Exception as e:
        return jsonify(error=str(e))    

@app.route('/actor/<_id>', methods = ['DELETE'])
def remove_actor(_id):
    try:
        actor = Actor.query.filter_by(actor_id=_id).first()
        db.session.delete(actor)
        db.session.commit()
        return jsonify(actor_id=_id)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/film/<_id>', methods=['GET'])
def get_film_by_id(_id):
    try:
        film = Film.query.filter_by(film_id=_id).first()
        film.film_actors = [item.actor_id for item in film.film_actor]
        return jsonify(film_schema.dump(film))
    except Exception as e:
        return jsonify(error=str(e))

#COUNTRY

@app.route('/country', methods = ['GET'])
def get_country():
    try:
        countries = Country.query.all()
        return jsonify(data=countries_schema.dump(countries))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/country/<_id>', methods = ['GET'])
def get_country_by_id(_id):
    try:
        country = Country.query.filter_by(country_id = _id).first()
        return jsonify(country_schema.dump(country))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/country/<_id>', methods = ['PUT'])
def update_country(_id):
    body = request.json
    country = body.get('country')
    try:
        tbcountry = Country.query.filter_by(country_id=_id).first()
        tbcountry.country = country
        db.session.commit()
        return jsonify(country_schema.dump(tbcountry))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/country/add', methods = ['POST'])
def country_add():
    body = request.json
    country = body.get('country')
    try:
        tbcountry = Country(country)
        db.session.add(tbcountry)
        db.session.commit()
        return jsonify(country_schema.dump(tbcountry))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/country/<_id>', methods = ['DELETE'])
def remove_country_by_id(_id):
    try:
        country = Country.query.filter_by(country_id=_id).first()
        db.session.delete(country)
        db.session.commit()
        return jsonify(country_id=_id)
    except Exception as e:
        return jsonify(error=str(e))

if __name__== '__main__':
    app.run(debug=True)
