# Create your tests here.
import unittest
from app.extensions import app, db, bcrypt
from app.models import User, Meal, Schedule
from datetime import date
from app.auth.routes import auth
from app.main.routes import main
from datetime import date

app.register_blueprint(auth)
app.register_blueprint(main)

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='user1', password=password_hash)
    db.session.add(user)
    db.session.commit()

def create_meals():
    meal1 = Meal(
        name='Pizza',
        ingredients='Dough, Tomato Sauce, Pepperoni',
        instructions='1. Make dough, 2. add sauce and toppings, 3. Bake in the oven.'
    )
    db.session.add(meal1)

    meal2 = Meal(
        name='Scrambled Eggs',
        ingredients='Eggs',
        instructions='1. Heat pan, 2. Beat eggs, 3. Scramble eggs in pan.'
    )
    db.session.add(meal2)
    db.session.commit()

def create_schedules():
    password_hash = bcrypt.generate_password_hash('password2').decode('utf-8')
    schedule1 = Schedule(
        meal_date = date(2024, 3, 4),
        user = User(username='user2', password=password_hash),
        meal = Meal(
        name='Scrambled Eggs',
        ingredients='Eggs',
        instructions='1. Heat pan, 2. Beat eggs, 3. Scramble eggs in pan.'
    )
    )
    db.session.add(schedule1)
    db.session.commit()


class MainTests(unittest.TestCase):    
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.context = app.app_context()
        self.context.push() 
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the login show up on the homepage."""
        create_user()
        create_meals()
        create_schedules()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('<a href="/login">Log In</a>', response_text)

        self.assertNotIn('<a href="/signout">Sign Out</a>', response_text)
    
    def test_homepage_logged_in(self):
        create_user()
        create_meals()
        create_schedules()
        login(self.app, 'user2', 'password2')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('March 04, 2024', response_text)
        self.assertIn('Scrambled Eggs', response_text)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_update_meal(self):
        app.config['LOGIN_DISABLED'] = True
        create_meals()

        update_data = {
            'name': 'Burrito',
            'ingredients': 'Tortilla, Beans, Meat, Sauce',
            'instructions': '1. Prep ingredients, 2. Wrap into burrito'
        }
        self.app.post('/meal_details/1', data=update_data)

        meal = Meal.query.filter_by(id=1).first()
        self.assertEqual(meal.name, 'Burrito')
        self.assertEqual(meal.ingredients, 'Tortilla, Beans, Meat, Sauce')
        self.assertEqual(meal.instructions, '1. Prep ingredients, 2. Wrap into burrito')
    
    def test_create_meal(self):
        app.config['LOGIN_DISABLED'] = True

        new_meal = {
            'name': 'Udon',
            'ingredients': 'Dashi broth, Udon noodles, toppings',
            'instructions': '1. Bring water to a boil, add udon noodles to cook. 2.Strain, add noodles to broth, add toppings.'
        }
        self.app.post('/add_meal', data=new_meal)
        meal = Meal.query.filter_by(name='Udon').first()
        self.assertEqual(meal.name, 'Udon')
        self.assertEqual(meal.ingredients, 'Dashi broth, Udon noodles, toppings')
        self.assertEqual(meal.instructions, '1. Bring water to a boil, add udon noodles to cook. 2.Strain, add noodles to broth, add toppings.')

    def test_delete_meal(self):
        app.config['LOGIN_DISABLED'] = True
        create_meals()
        response = self.app.post('/delete_meal/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        deleted_meal = Meal.query.get(1)
        self.assertIsNone(deleted_meal)

        


    


    
