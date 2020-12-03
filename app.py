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
from models import Actor, ActorSchema, Film, FilmSchema, Country, CountrySchema, City, CitySchema, CityCountrySchema

#global variable
actors_schema = ActorSchema(many=True)
actor_schema = ActorSchema()
film_schema = FilmSchema()
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
city_schema = CitySchema()
cities_schema = CitySchema(many=True)
city_country_schema = CityCountrySchema()

@app.route('/index', methods = ['GET'])
def index():
    return 'Hello World'

#ACTOR

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

#FILM

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

@app.route('/city/country/<_id>', methods = ['GET'])
def get_city_by_country_id(_id):
    try:
        country = Country.query.filter_by(country_id=_id).first()
        country.country_cities = [item.city for item in country.country_city]
        return jsonify(city_country_schema.dump(country))
    except Exception as e:
        return jsonify(error=str(e))

#CITY

@app.route('/city', methods = ['GET'])
def get_city():
    try:
        cities = City.query.all()
        return jsonify(data=cities_schema.dump(cities))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/country/city/<_id>', methods = ['GET'])
def get_country_by_city(_id):
    try:
        city = City.query.filter_by(city_id = _id).first()
        return jsonify(city_id = city.city_id, city_name = city.city, country_id = city.country_id, country_name = city.city_country.country)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/city/<_id>', methods = ['GET'])
def get_city_by_id(_id):
    try:
        city = City.query.filter_by(city_id = _id).first()
        return jsonify(city_schema.dump(city))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/city/<_id>', methods = ['PUT'])
def update_city(_id):
    body = request.json
    city = body.get('city')
    try:
        tbcity = City.query.filter_by(city_id=_id).first()
        tbcity.city = city
        db.session.commit()
        return jsonify(city_schema.dump(tbcity))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/city/add', methods = ['POST'])
def city_add():
    body = request.json
    city = body.get('city')
    country_id = body.get('country_id')
    try:
        tbcity = City(city, country_id)
        db.session.add(tbcity)
        db.session.commit()
        return jsonify(city_schema.dump(tbcity))
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/city/<_id>', methods = ['DELETE'])
def remove_city_by_id(_id):
    try:
        city = City.query.filter_by(city_id=_id).first()
        db.session.delete(city)
        db.session.commit()
        return jsonify(city_id=_id)
    except Exception as e:
        return jsonify(error=str(e))

if __name__== '__main__':
    app.run(debug=True)
