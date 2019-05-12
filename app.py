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
import resources.UserResources as user
import resources.ExerciseResources as exercise

api.add_resource(user.UserRegistration, '/signUp')
api.add_resource(user.UserUpdate, '/updateUser')
api.add_resource(user.UserLogin, '/login')
api.add_resource(user.AllUsers, '/users')
api.add_resource(user.AllUsersNotFriend, '/usersNotFriend')
api.add_resource(user.GetFriends, '/friends')
api.add_resource(user.GetFriendshipRequest, '/friendRequest')
api.add_resource(user.SendFriendshipRequest, '/addFriend/<friend>')
api.add_resource(user.AcceptFriendshipRequest, '/acceptFriend/<friend>')
api.add_resource(user.RejectFriendshipRequest, '/rejectFriend/<friend>')
api.add_resource(user.RemoveFriendshipRequest, '/removeFriendship/<friend>')
api.add_resource(exercise.SecretResource, '/secret')
api.add_resource(exercise.GetAllExercises, '/exercises')
api.add_resource(exercise.InitExerciseResolution, '/initResolution')
api.add_resource(exercise.SendKnapsackExercise, '/knapsack')
api.add_resource(exercise.GetMyResolutions, '/myResolutions')
api.add_resource(exercise.GetBestResolutionsByExercise, '/bestResolutions/<exercise_id>')
