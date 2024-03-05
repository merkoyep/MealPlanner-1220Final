# Create your tests here.
# Create your tests here.
import os
from unittest import TestCase
from app.extensions import app, db, bcrypt
from app.models import User, Meal, Schedule
from app.auth.routes import auth
from app.main.routes import main
from datetime import date

app.register_blueprint(auth)
app.register_blueprint(main)

class AuthTests(TestCase):
    """Testing authentication (signup, login, logout)"""

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

    
    def test_signup(self):
        """Testing signup flow."""
        form_data = {
            'username': 'testcaseuser',
            'password': 'testingpassword'
        }
        res = self.app.post('/signup', data=form_data)
        self.assertEqual(res.status_code, 302)

        user = User.query.filter_by(username='testcaseuser').first()
        self.assertIsNotNone(user)

    def test_signup_existing_user(self):
        """Testing error for existing user."""
        self.test_signup()
        form_data = {
            'username': 'testcaseuser',
            'password': 'testingpassword'
        }
        res = self.app.post('/signup', data=form_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'That username is taken. Please chose a different one.', res.data)
    
    def test_login_correct_password(self):
        """Testing proper login."""
        form_data = {
            'username': 'testcaseuser',
            'password': 'testingpassword'
        }
        self.app.post('/signup', data=form_data)
        res = self.app.post('/login', data=form_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('<a href="/login">Log In</a>', res.data.decode('utf-8'))

    def test_login_incorrect_password(self):
        """Testing incorrect password error."""
        hashed_password = bcrypt.generate_password_hash('password1').decode('utf-8')
        existing_user = User(username='forgetfulUser', password=hashed_password)
        db.session.add(existing_user)
        db.session.commit()
        form_data = {
            'username': 'forgetfulUser',
            'password': 'password34'
        }
        res = app.test_client().post('/login', data=form_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Password doesn&#39;t match. Please try again', res.data.decode('utf-8'))

    def test_logout(self):
        """Testing logout functionality."""
        hashed_password = bcrypt.generate_password_hash('password1').decode('utf-8')
        existing_user = User(username='logoutuser', password=hashed_password)
        db.session.add(existing_user)
        db.session.commit()
        form_data = {
            'username': 'logoutuser',
            'password': hashed_password
        }
        app.test_client().post('/login', data=form_data)
        res = app.test_client().get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<a href="/login">Log In</a>', res.data.decode('utf-8'))