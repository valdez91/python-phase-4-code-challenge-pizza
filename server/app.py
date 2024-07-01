#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import os

# Directory setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Flask app setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Database migration setup
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(rules=['-restaurant_pizzas']) for restaurant in restaurants]), 200

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_or_delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    if request.method == 'GET':
        return jsonify(restaurant.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({}), 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(rules=['-restaurant_pizzas']) for pizza in pizzas]), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as e:
        return jsonify({'errors': ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)