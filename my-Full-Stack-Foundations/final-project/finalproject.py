from flask import Flask, render_template, flash, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from FakeMenuItems import *

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    if len(restaurants) == 0:
        flash('No restaurant registered!')
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurants/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash('New restaurant added!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('Restaurant updated!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant deleted!')
        return redirect(url_for('showRestaurants'))
    else:
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
