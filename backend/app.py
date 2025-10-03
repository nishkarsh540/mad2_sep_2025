from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_identity, unset_jwt_cookies
from model import db, User,Category
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'vehicle'


db.init_app(app)
CORS(app,origins='*')

jwt = JWTManager(app)
api = Api(app)


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role', 'user')

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message":"Username already exists"}), 400
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        user_info = {
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        return jsonify(access_token=access_token, user_info=user_info), 200
    else:
        return jsonify({"message":"Invalid credentials"}), 401


class CategoryResource(Resource):
    def get(self):
        # role = get_jwt_identity()['role']
        # if role != 'admin':
        #     return jsonify({"message":"Admin access required"}), 403

        categories = Category.query.all()
        category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
        print(category_list)
        return (category_list), 200

    def post(self):
        name = request.json.get('name')
        if Category.query.filter_by(name=name).first() is not None:
            return jsonify({"message":"Category already exists"}), 400  
        
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message":"Category created successfully"}), 201

api.add_resource(CategoryResource, '/categories')

if __name__ == '__main__':
    app.run(debug=True)