from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.model import User

"""This script contains all forms for the CookBook web application"""


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 150)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    method = TextAreaField('Method', validators=[DataRequired()])
    meal = SelectField('Meal', validators=[DataRequired()],
                       choices=[('breakfast', 'Breakfast'),
                                ('lunch', 'Lunch'),
                                ('starter', 'Starter'),
                                ('main', 'Main Course'),
                                ('dessert', 'Dessert'),
                                ('drink', 'Drink')])
    public = BooleanField('Available to public', default="checked")
    submit1 = SubmitField('Submit')


# Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Currently unused features
# Thumbnail/Image upload
class PhotoForm(FlaskForm):
    photo = FileField("Upload a thumbnail", validators=[FileRequired()])
    submit2 = SubmitField("Upload")

