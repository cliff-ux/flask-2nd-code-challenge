from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.pizza.restaurants',)
    serialize_only = ('id', 'name', 'address')
    

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.pizza.restaurants',)
    serialize_only = ('id', 'name', 'ingredients')


    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')


    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError('Price must be between 1 and 30')
        return price

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'













































































































# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)


# class Restaurant(db.Model, SerializerMixin):
#     __tablename__ = 'restaurants'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     address = db.Column(db.String)

#     # add relationship
#     pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')


#     # add serialization rules
#     serialize_rules = ('-pizzas.restaurants',)
#     serialize_only = ('id', 'name', 'address')
    

#     def __repr__(self):
#         return f'<Restaurant {self.name}>'


# class Pizza(db.Model, SerializerMixin):
#     __tablename__ = 'pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     ingredients = db.Column(db.String)

#     # add relationship
#     restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')
#     serialize_rules = ('-restaurants.pizzas',)
#     serialize_only = ('id', 'name', 'ingredients')


#     # add serialization rules
#     serialize_rules = ('-restaurants.pizzas',)
#     serialize_only = ('id', 'name', 'ingredients')


#     def __repr__(self):
#         return f'<Pizza {self.name}, {self.ingredients}>'


# class RestaurantPizza(db.Model, SerializerMixin):
#     __tablename__ = 'restaurant_pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer, nullable=False)

#     # add relationships
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
#     pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
#     restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
#     pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
#     serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)
#     serialize_only = ('id', 'price', 'pizza_id', 'restaurant_id')


#     # add serialization rules
#     serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)
#     serialize_only = ('id', 'price', 'pizza_id', 'restaurant_id')
#     validates('price', lambda price: 1 <= price <= 30, 'Price must be between 1 and 30')


#     # add validation
#     @validates('price')
#     def validate_price(self, key, price):
#         if not 1 <= price <= 30:
#             raise ValueError('Price must be between 1 and 30')
#         return price
#     def save(self):
#         db.session.add(self)
#         db.session.commit()
    

#     def __repr__(self):
#         return f'<RestaurantPizza ${self.price}>'
