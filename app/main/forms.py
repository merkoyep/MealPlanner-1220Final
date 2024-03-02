# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length

class MealForm(FlaskForm):
    """Form to create new meal"""
    name = StringField('Name', validators=[DataRequired(),Length(min=3, max=80, message="Your meal name must have 3-80 chars.")])
    ingredients = TextAreaField('Ingredients', [DataRequired()])
    instructions = TextAreaField('Instructions', [DataRequired()])
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    """Form to delete an item"""
    delete = SubmitField('Delete')

class ScheduleForm(FlaskForm):
    """Form to add scheduled meals"""
    meal_date = DateField('Meal Date', validators=[DataRequired()])
    meal = SelectField('Meal', choices=[], coerce=int)
    submit = SubmitField('Submit')
