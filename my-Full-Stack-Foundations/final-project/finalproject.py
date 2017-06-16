from flask import Flask, render_template
from FakeMenuItems import *

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurants/new/')
def newRestaurant():
    return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
def showMenu(restaurant_id):
    return "Restaurant %s menu item list" % restaurant_id


@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "Add new menu item to restaurant %s" % restaurant_id


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
    return "Edit menu item %s from restaurant %s" % (item_id, restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
    return "Delete menu item %s from restaurant %s" % (item_id, restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
