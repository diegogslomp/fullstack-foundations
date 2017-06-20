from flask import Flask, render_template, flash
from FakeMenuItems import *

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    flash('Message for empty restaurant list')
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
    flash('Message for empty menu list')
    return render_template('menu.html', items = items)


@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return render_template('newMenuItem.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
    return render_template('editMenuItem.html', item = item)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
    return render_template('deleteMenuItem.html', item = item)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
