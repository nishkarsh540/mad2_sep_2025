from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    # 'user' or 'admin'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


with app.app_context():
    db.create_all()

    if User.query.filter_by(username='admin').first() is None:
        admin_password = generate_password_hash('admin123')
        admin_user = User(username='admin', email='admin@example.com', password=admin_password, role='admin')
        db.session.add(admin_user)
        db.session.commit()
    else:
        print("Admin user already exists.")

    if Category.query.count() == 0:
        category_name = 'Fruits'
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
    else:
        print("Categories already exist.")