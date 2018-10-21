from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

#Create
'''
myFirstRestaurant = Restaurant(name="Sandwich Haven")
session.add(myFirstRestaurant)
session.commit()

bigsandwich = MenuItem(
    name="Big Sandwich",
    description="It's fairly large.",
    course="Entree",
    price="$9.99",
    restaurant=myFirstRestaurant)

session.add(bigsandwich)
session.commit()
'''

#Read
firstResult = session.query(Restaurant).first()
print(firstResult)

restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print(restaurant.name)

menu_items = session.query(MenuItem).all()
for menu_item in menu_items:
    print(menu_item.name)

#Update
veggie_burgers = session.query(MenuItem).filter_by(
    name="Veggie Burger")

for veggie_burger in veggie_burgers:
    print(veggie_burger.id)
    print(veggie_burger.price)
    print(veggie_burger.restaurant.name)
    print("\n")

urban_veggie_burger = session.query(MenuItem).filter_by(
    id=9).one()
print(urban_veggie_burger.price)
urban_veggie_burger.price = "$2.99"
session.add(urban_veggie_burger)
session.commit()

for veggie_burger in veggie_burgers:
    print(veggie_burger.id)
    print(veggie_burger.price)
    print(veggie_burger.restaurant.name)
    print("\n")

for veggie_burger in veggie_burgers:
    if veggie_burger.price != "$2.99":
        veggie_burger.price = "$2.99"
        session.add(veggie_burger)
        session.commit()

#Delete
spinach = session.query(MenuItem).filter_by(
    name="Spinach Ice Cream").one()

print(spinach.restaurant.name)
session.delete(spinach)
session.commit()

spinach = session.query(MenuItem).filter_by(
    name="Spinach Ice Cream").one()