from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://pepe:pepe@localhost/alg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'stringsecret'
db = SQLAlchemy(app)

import models.models



@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


CORS(app)





import views.views
import resources.resources as res

api.add_resource(res.UserRegistration, '/signUp')
api.add_resource(res.UserLogin, '/login')
api.add_resource(res.UserLogoutAccess, '/logout/access')
api.add_resource(res.UserLogoutRefresh, '/logout/refresh')
api.add_resource(res.TokenRefresh, '/token/refresh')
api.add_resource(res.AllUsers, '/users')
api.add_resource(res.SecretResource, '/secret')
api.add_resource(res.GetAllExercises, '/exercises')

