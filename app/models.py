# Create your models here.
# Create your models here.
from app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    schedules = db.relationship('Schedule', back_populates='user')
    
    def __str__(self):
        return f'<User: {self.username}>'

    def __repr__(self):
        return f'<User: {self.username}>'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    user = db.relationship('User', back_populates='schedules')
    meal = db.relationship('Meal', back_populates='schedules')

    def __str__(self):
        return f'<Schedule: {self.meal_date}>'

    def __repr__(self):
        return f'<Schedule: {self.meal_date}>'
    

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.Text(), nullable=False)
    instructions = db.Column(db.Text(), nullable=False)

    schedules = db.relationship('Schedule', back_populates='meal')

    def __str__(self):
        return f'<Meal: {self.name}>'

    def __repr__(self):
        return f'<Meal: {self.name}>'

