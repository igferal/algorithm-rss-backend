from app import db
from passlib.hash import pbkdf2_sha256 as sha256

friendship = db.Table('friendship',
                      db.Column('first_friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                      db.Column('second_friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                      )

friendship_request = db.Table('friendship_request',
                              db.Column('first_friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                              db.Column('second_friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                              )


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    friendship = db.relation(
        'UserModel', secondary=friendship,
        primaryjoin=friendship.c.first_friend_id == id,
        secondaryjoin=friendship.c.second_friend_id == id,
        backref="user_friend")
    resolutions = db.relationship('Resolution')
    friendship_request = db.relation(
        'UserModel', secondary=friendship_request,
        primaryjoin=friendship_request.c.first_friend_id == id,
        secondaryjoin=friendship_request.c.second_friend_id == id,
        backref="user_friend_request")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



    @classmethod
    def update_user(cls, user, data):
        user.name = data["name"]
        user.surname = data["surname"]
        if data["password"] != "":
            user.password = UserModel.generate_hash(data['newPassword'])
        user.email = data["email"]
        db.session.commit()
        return user

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def add_friendship_request(cls, username, friend_id):

        current = cls.query.filter_by(username=username).first()
        friend = cls.query.filter_by(id=friend_id).first()

        if current in friend.friendship or current in friend.friendship_request:
            return False
        else:
            friend.friendship_request.append(current)
            db.session.commit()
            return True

    @classmethod
    def reject_friendship_request(cls, username, friend_id):
        current = cls.query.filter_by(username=username).first()
        friend = cls.query.filter_by(id=friend_id).first()
        current.friendship_request.remove(friend)
        db.session.commit()
        return current

    @classmethod
    def remove_friendship(cls, username, friend_id):
        current = cls.query.filter_by(username=username).first()
        friend = cls.query.filter_by(id=friend_id).first()
        current.friendship.remove(friend)
        friend.friendship.remove(current)
        db.session.commit()
        return current

    @classmethod
    def accept_friendship_request(cls, username, friend_id):
        current = cls.query.filter_by(username=username).first()
        friend = cls.query.filter_by(id=friend_id).first()
        current.friendship.append(friend)
        friend.friendship.append(current)
        current.friendship_request.remove(friend)
        db.session.commit()
        return current

    @classmethod
    def get_friendship_requests(cls, username):
        current = cls.query.filter_by(username=username).first()
        return list(map(lambda x: cls.to_json(x), current.friendship_request))

    @classmethod
    def get_friends(cls, username):
        current = cls.query.filter_by(username=username).first()
        return list(map(lambda x: cls.to_json(x), current.friendship))

    @staticmethod
    def to_json(x):
        return {
            'id': x.id,
            'username': x.username,
            'name': x.name,
            'surname': x.surname,
            'email': x.email
        }

    @classmethod
    def return_all(cls):

        return list(map(lambda x: cls.to_json(x), UserModel.query.all()))

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
