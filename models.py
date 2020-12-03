from app import db, ma
import datetime

class Actor(db.Model):
    __tablename__ = 'actor'

    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
    def __repr__(self):
        return '<actor id {}>'.format(self.actor_id)

class Country(db.Model):
    __tablename__ = 'country'

    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String())
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())
    country_city = db.relationship('City', backref='Country', lazy=True)
    country_cities = db.ARRAY(db.Integer)

    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return '<country id {} and city id {}>'.format(self.country_id, self.city_id)

class City(db.Model):
    __tablename__ = 'city'

    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())
    city_country = db.relationship('Country', backref='City', lazy=True)

    def __init__(self, city, country_id):
        self.city = city
        self.country_id = country_id

    def __repr__(self):
        return '<city_id {}>'.format(self.city_id)

class Address(db.Model):
    __tablename__='address'

    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    address2 = db.Column(db.String())
    district = db.Column(db.String())
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())
    addresses_city = db.ARRAY(db.Integer)

    def __init__(self, address, address2, district, city_id, postal_code, phone):
        self.address = address
        self.address2 = address2
        self.district = district
        self.city_id = city_id
        self.postal_code = postal_code
        self.phone = phone
    
    def __repr__(self):
        return '<address_id {}>'.format(self.address_id)

class Film(db.Model):
    __tablename__='film'

    film_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    release_year = db.Column(db.Integer)
    language_id = db.Column(db.SmallInteger)
    rental_duration = db.Column(db.SmallInteger)
    rental_rate = db.Column(db.Numeric)
    length = db.Column(db.SmallInteger)
    replacement_cost = db.Column(db.Numeric)
    rating = db.Column(db.String())
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())
    special_features = db.ARRAY(db.String())
    film_actor = db.relationship('FilmActor', cascade="all,delete", backref='film', lazy=True)
    film_actors = db.ARRAY(db.Integer)

    def __init__(self, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, special_features):
        self.title = title
        self.description = description
        self.release_year = release_year
        self.language_id = language_id
        self.rental_duration = rental_duration
        self.rental_rate = rental_rate
        self.length = length
        self.replacement_cost = replacement_cost
        self.rating = rating
        self.special_features = special_features
        
    def __repr__(self):
        return '<film id {}>'.format(self.film_id)

class FilmActor(db.Model):
    __tablename__ = 'film_actor'

    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'),primary_key=True, nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True, nullable=False)

    def __repr__(self):
        return '<film id {} AND actor_id {}>'.format(self.actor_id, self.film_id)

class ActorSchema(ma.Schema):
    class Meta:
        fields = ("actor_id", "first_name", "last_name", "last_update")
        model = Actor

class FilmSchema(ma.Schema):
    class Meta:
        fields = ("film_id", "title", "description", "release_year", "film_actors")
        model = Film

class FilmActorSchema(ma.Schema):
    class Meta:
        fields = ("film_id", "actor_id")
        model = FilmActor

class CountrySchema(ma.Schema):
    class Meta:
        fields = ("country_id", "country", "last_update")
        model = Country

class CityCountrySchema(ma.Schema):
    class Meta:
        fields = ("country_id", "country", "last_update", "country_cities")
        model = Country

class CitySchema(ma.Schema):
    class Meta:
        fields = ("city_id", "city", "country_id", "last_update")
        model = City

class AddressSchema(ma.Schema):
    class Meta:
        fields = ("address_id", "address", "address2", "district", "city_id", "postal_code", "phone", "last_update")
        model = Address

class Address2Schema(ma.Schema):
    class Meta:
        fields = ("address", "city_id")
        model = Address