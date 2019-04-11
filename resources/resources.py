import datetime

from flask_restful import Resource, reqparse
from models.exercise import Exercise, Heuristic
from models.user import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('name', help='This field cannot be blank', required=True)
        parser.add_argument('surname', help='This field cannot be blank', required=True)

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            email=data['email'],
            name=data['name'],
            surname=data['surname'],

        )

        try:
            new_user.save_to_db()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'], expires_delta=expires)
            return {
                'user': {'name': new_user.name, 'surname': new_user.surname, 'username': new_user.username,
                         'email': new_user.email},
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'], expires_delta=expires)
            return {
                'user': {'name': current_user.name, 'surname': current_user.surname, 'username': current_user.username,
                         'email': current_user.email},
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserUpdate(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='Send Password', required=False)
        parser.add_argument('newPassword', help='Send Password', required=False)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('name', help='This field cannot be blank', required=True)
        parser.add_argument('surname', help='This field cannot be blank', required=True)

        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if UserModel.verify_hash(data['password'], user.password):

            user = UserModel.update_user(user, data)

            try:
                expires = datetime.timedelta(days=365)
                access_token = create_access_token(identity=data['username'], expires_delta=expires)
                refresh_token = create_refresh_token(identity=data['username'], expires_delta=expires)
                return {
                    'user': {'name': user.name, 'surname': user.surname, 'username': user.username,
                             'email': user.email},
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            except:
                return {'message': 'No se pudo actualizar el usuario'}, 500
        else:
            return {'message': 'Incorrect Password'}, 200


class SendFriendshipRequest(Resource):
    @jwt_required
    def get(self, friend):
        current_user = get_jwt_identity()
        try:
            UserModel.add_friendship_request(current_user, friend)
            return {'message': 'Request Sent'}
        except:
            return {'message': 'Error sending requeste'}


class GetFriendshipRequest(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            return {'friendRequests': UserModel.get_friendship_requests(current_user)}
        except:
            return {'message': 'Error sending requeste'}


class GetFriends(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            return {'friends': UserModel.get_friends(current_user)}
        except:
            return {'message': 'Error sending request'}


class AcceptFriendshipRequest(Resource):
    @jwt_required
    def get(self, friend):
        current_user = get_jwt_identity()
        try:
            UserModel.accept_friendship_request(current_user, friend)
            return {'message': 'Request Sent'}
        except:
            return {'message': 'Error sending request'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class GetAllExercises(Resource):
    @jwt_required
    def get(self):
        try:
            return Exercise.return_all()
        except:
            return {'Token': False}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'users': list(filter(lambda x: x['username'] != current_user, UserModel.return_all()))}

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
