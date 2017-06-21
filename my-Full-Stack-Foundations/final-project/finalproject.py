from flask import Flask, render_template, flash, url_for, request, redirect, jsonify
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
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/JSON/')
def jsonRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify([r.serialize for r in restaurants])


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


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
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
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant deleted!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showRestaurantMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if len(items) == 0:
        flash('Empty menu list!')
    return render_template('restaurantMenu.html', restaurant_id=restaurant_id, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def jsonRestaurantMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify([i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_menu_item = MenuItem(name=request.form['name'], description=request.form['description'],
                                 price=request.form['price'], course=request.form['course'],
                                 restaurant_id=restaurant_id,)
        session.add(new_menu_item)
        session.commit()
        flash('New menu item created!')
        return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.price = request.form['course']
        session.add(item)
        session.commit()
        flash('Menu item edited!')
        return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', item=item, restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON/', methods=['GET','POST'])
def jsonMenuItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(item.serialize)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item deleted!')
        return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=item, restaurant_id=restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
