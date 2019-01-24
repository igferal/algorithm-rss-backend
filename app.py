from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://pepe:pepe@localhost/alg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

import models


db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
CORS(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


import views.views
import resources.resources as res

api.add_resource(res.UserRegistration, '/registration')
api.add_resource(res.UserLogin, '/login')
api.add_resource(res.UserLogoutAccess, '/logout/access')
api.add_resource(res.UserLogoutRefresh, '/logout/refresh')
api.add_resource(res.TokenRefresh, '/token/refresh')
api.add_resource(res.AllUsers, '/users')
api.add_resource(res.SecretResource, '/secret')
