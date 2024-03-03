from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db, app
from app.models import Meal, Schedule, User
from app.main.forms import MealForm, DeleteForm, ScheduleForm
main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    if current_user.is_authenticated:
        schedules = Schedule.query.filter_by(user_id=current_user.id).order_by(Schedule.meal_date).all()
    else:
        schedules = []
    return render_template('home.html', schedules=schedules)

@main.route('/add_meal', methods=['GET', 'POST'])
@login_required
def add_meal():
    form = MealForm()

    if form.validate_on_submit():
        mealname = form.name.data
        existing_meal = Meal.query.filter_by(name=mealname).first()
        if existing_meal:
            flash('Meal already exists.')
            return redirect(url_for('main.add_meal'))
        else:
            new_meal = Meal(
                name=form.name.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data
            )
            db.session.add(new_meal)
            db.session.commit()
            flash(f"{new_meal.name} has been added.")
            return redirect(url_for('main.all_meals'))
    return render_template('addmeal.html', form=form)

@main.route('/all_meals')
@login_required
def all_meals():
    all_meals = Meal.query.all()
    return render_template('meals.html', all_meals=all_meals)

@main.route('/meal_details/<meal_id>', methods=['GET', 'POST'])
@login_required
def meal_details(meal_id):
    meal = Meal.query.get(meal_id)
    form = MealForm(obj=meal)

    if form.validate_on_submit():
        print('after validation')
        meal.name = form.name.data
        meal.ingredients = form.ingredients.data
        meal.instructions = form.instructions.data
        db.session.commit()
        flash('Meal updated.')
        return redirect(url_for('main.meal_details', meal_id=meal_id))
    meal = Meal.query.get(meal.id)
    return render_template('mealdetails.html', form=form, meal=meal)

@main.route('/delete_meal/<meal_id>', methods=['GET', 'POST'])
def delete_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(meal)
        db.session.commit()
        flash(f'{meal.name} has been deleted.')
        return redirect(url_for('main.all_meals'))
    
    return render_template('deletemeal.html', meal=meal, form=form)

@main.route('/add_schedule', methods=['GET','POST'])
def add_schedule():
    form = ScheduleForm()
    form.meal.choices = [(meal.id, meal.name) for meal in Meal.query.all()]
    print('before validation')
    if form.validate_on_submit():
        print('after validation')
        print(f'{form.meal_date.data}, {form.meal.data}')
        new_schedule = Schedule(
            meal_date=form.meal_date.data, 
            meal_id=form.meal.data,
            user_id=current_user.id
            )
        db.session.add(new_schedule)
        db.session.commit()
        print('committed')
        flash('Schedule added successfully!')
        return redirect(url_for('main.homepage'))
    
    return render_template('addschedule.html', form=form)

@main.route('/delete_schedule/<schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    form = DeleteForm()
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if form.validate_on_submit():
        db.session.delete(schedule)
        db.session.commit()
        flash(f'The schedule for {schedule.meal_date} has been deleted.')
        return redirect(url_for('main.homepage'))
    
    return render_template('deleteschedule.html', schedule=schedule, form=form)


