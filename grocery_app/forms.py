from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app.models import ItemCategory, GroceryStore, GroceryItem, User

class SignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # check if username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is None:
    #         raise ValidationError("NO user with that username. Please try loging in again")

    # def validate_password(self, password):
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if not bcrypt.check_password_hash(user.password, password_field.data):
    #         raise ValidationError("Password did not match")

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # title = StringField('Title')
    # Getting error whenever bottom line is uncommented
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=50)])

    # - address - StringField
    address = StringField("Address", validators=[DataRequired(), Length(min=5, max=50)])
    
    # - submit button
    submit = SubmitField("Submit")
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    name = StringField("Item Name", validators=[DataRequired(), Length(min=4, max=30)])

    # - price - FloatField
    price = FloatField("Item Price", validators=[DataRequired()])

    # - category - SelectField (specify the 'choices' param)
    # import ItemCategory from models
    category = SelectField("Item Category", choices=ItemCategory.choices())

    # - photo_url - StringField (use a URL validator)
    photo_url = StringField("Photo URL", validators=[URL(require_tld=True)])

    # - store - QuerySelectField (specify the `query_factory` param)
    # what is lambda, import GroceryStore to be able to query
    store = QuerySelectField("Grocery Store", query_factory=lambda: GroceryStore.query)

    # - submit button
    submit = SubmitField("Submit")
