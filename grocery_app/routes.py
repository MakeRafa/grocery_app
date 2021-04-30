from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from datetime import date, datetime

from grocery_app.models import GroceryStore, GroceryItem, User
# from grocery_app.forms import BookForm, AuthorForm, GenreForm
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm
# Import app and db from events_app package so that we can run app
from grocery_app import app, db, bcrypt

main = Blueprint("main", __name__)

auth = Blueprint("auth",__name__)

##########################################
#           Login/Signup Routes          #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # print('in signup')

    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created!')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            print('Account logged in!')
            return redirect(next_page if next_page else url_for('main.homepage'))

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
            )

        db.session.add(new_store)
        db.session.commit()

        flash('New grocery store has been created!')

    # TODO: Send the form to the template and use it to render the form fields
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()

    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New grocery item has been created!')
    # TODO: Send the form to the template and use it to render the form fields
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    # store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    store = GroceryStore.query.get(store_id)

    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data

        # # db.session.add(store)
        db.session.commit()

        flash('Grocery store has been updated!')
    # TODO: Send the form to the template and use it to render the form fields
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    item = GroceryItem.query.get(item_id)

    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        
        # db.session.add(item)
        db.session.commit()

        flash('Item has been updated!')
        return redirect(url_for('main.item_detail', item_id=item.id))
    # TODO: Send the form to the template and use it to render the form fields
    # item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form=form)

