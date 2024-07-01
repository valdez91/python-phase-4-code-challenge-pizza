from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.restaurant_id', '-restaurant_pizzas.pizza_id', '-restaurant_pizzas.pizza.restaurants')

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    serialize_rules = ('-restaurant_pizzas.pizza', '-restaurant_pizzas.pizza_id', '-restaurant_pizzas.restaurant_id', '-restaurant_pizzas.restaurant.pizzas')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, ForeignKey('pizzas.id', ondelete='CASCADE'), nullable=False)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)

    pizza = relationship('Pizza', backref='restaurant_pizzas')
    restaurant = relationship('Restaurant', backref='restaurant_pizzas')

    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("validation errors")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"