#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, abort
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants]

class Restaurant(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas'))
        else:
            return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return "", 204
        else:
            return {"error": "Restaurant not found"}, 404

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas]

class CreateRestaurantPizza(Resource):
    def post(self):
        data = request.get_json()
        pizza = Pizza.query.get(data["pizza_id"])
        restaurant = Restaurant.query.get(data["restaurant_id"])
        if pizza and restaurant:
            try:
                restaurant_pizza = RestaurantPizza(price=data["price"], pizza=pizza, restaurant=restaurant)
                restaurant_pizza.save()
                return restaurant_pizza.to_dict(only=('id', 'pizza', 'pizza_id', 'price', 'restaurant', 'restaurant_id'))
            except ValueError as e:
                return {"errors": [str(e)]}, 400
        else:
            return {"error": "Restaurant or Pizza not found"}, 404

api.add_resource(Restaurants, '/restaurants')
api.add_resource(Restaurant, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(CreateRestaurantPizza, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(debug=True)

























































































# #!/usr/bin/env python3

# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, make_response, jsonify, abort
# from flask_restful import Api, Resource
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)

# class Restaurants(Resource):
#     def get(self):
#         restaurants = Restaurant.query.all()
#         return [{"address": restaurant.address, "id": restaurant.id, "name": restaurant.name} for restaurant in restaurants]

# class Restaurant(Resource):
#     def get(self, id):
#         restaurant = Restaurant.query.get(id)
#         if restaurant:
#             return {
#                 "address": restaurant.address,
#                 "id": restaurant.id,
#                 "name": restaurant.name,
#                 "restaurant_pizzas": [
#                     {
#                         "id": rp.id,
#                         "pizza": {
#                             "id": rp.pizza.id,
#                             "ingredients": rp.pizza.ingredients,
#                             "name": rp.pizza.name
#                         },
#                         "pizza_id": rp.pizza_id,
#                         "price": rp.price,
#                         "restaurant_id": rp.restaurant_id
#                     } for rp in restaurant.restaurant_pizzas
#                 ]
#             }
#         else:
#             return {"error": "Restaurant not found"}, 404

#     def delete(self, id):
#         restaurant = Restaurant.query.get(id)
#         if restaurant:
#             db.session.delete(restaurant)
#             db.session.commit()
#             return "", 204
#         else:
#             return {"error": "Restaurant not found"}, 404

# class Pizzas(Resource):
#     def get(self):
#         pizzas = Pizza.query.all()
#         return [{"id": pizza.id, "ingredients": pizza.ingredients, "name": pizza.name} for pizza in pizzas]

# class CreateRestaurantPizza(Resource):
#     def post(self):
#         data = request.get_json()
#         pizza = Pizza.query.get(data["pizza_id"])
#         restaurant = Restaurant.query.get(data["restaurant_id"])
#         if pizza and restaurant:
#             if data["price"] < 1 or data["price"] > 30:
#                 return {"error": "Price must be between 1 and 30"}, 400
#             restaurant_pizza = RestaurantPizza(price=data["price"], pizza=pizza, restaurant=restaurant)
#             db.session.add(restaurant_pizza)
#             db.session.commit()
#             return {
#                 "id": restaurant_pizza.id,
#                 "pizza": {
#                     "id": restaurant_pizza.pizza.id,
#                     "ingredients": restaurant_pizza.pizza.ingredients,
#                     "name": restaurant_pizza.pizza.name
#                 },
#                 "pizza_id": restaurant_pizza.pizza_id,
#                 "price": restaurant_pizza.price,
#                 "restaurant": {
#                     "address": restaurant_pizza.restaurant.address,
#                     "id": restaurant_pizza.restaurant.id,
#                     "name": restaurant_pizza.restaurant.name
#                 },
#                 "restaurant_id": restaurant_pizza.restaurant_id
#             }
#         else:
#             return {"error": "Pizza or Restaurant not found"}, 404

# api.add_resource(Restaurants, '/restaurants')
# api.add_resource(Restaurant, '/restaurants/<int:id>')
# api.add_resource(Pizzas, '/pizzas')
# api.add_resource(CreateRestaurantPizza, '/restaurant_pizzas')

# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)














































































































# # #!/usr/bin/env python3

# # from models import db, Restaurant, RestaurantPizza, Pizza
# # from flask_migrate import Migrate
# # from flask import Flask, request, make_response
# # from flask_restful import Api, Resource
# # import os

# # BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# # DATABASE = os.environ.get(
# #     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.json.compact = False

# # migrate = Migrate(app, db)

# # db.init_app(app)


# # @app.route('/')
# # def index():
# #     return '<h1>Code challenge</h1>'


# # if __name__ == '__main__':
# #     app.run(port=5555, debug=True)
