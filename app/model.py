from flask import current_app, flash
from flask_login import login_manager, UserMixin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


# The user class defines the users database
# It contains functions to set password_hash, issue tokens for email confirmation and forgotten passwords.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # When passed a password stores it as a password_hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Used to verify the submitted password matches the password_hash in the database
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # generate email confirmation token using
    def generate_confirmation_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt='email-confirmation')

    # confirm token is valid
    def confirm(self, token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='email-confirmation', max_age=3600)
        except:
            return False
        if data != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # generate password_reset_token token using
    def generate_password_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt='password-reset')

    # confirm token is valid
    def confirm_password_reset(token, new_password):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='password-reset', max_age=600)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        user = User.query.filter_by(email=data).first()
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


@login_manager.user_loader
def load_user(self):
    return User.query.get(int(self))


# This class defines the recipe database
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    title = db.Column(db.String(128), unique=True)
    ingredients = db.Column(db.Text)
    method = db.Column(db.Text)
    public = db.Column(db.Boolean)
    meal = db.Column(db.String(25))
    author_id = db.Column(db.String(64), db.ForeignKey('users.username'))

    def __repr__(self):
        return '<Recipe %r>' % self.title


# Planned db to give users roles like a admin/moderator
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name




