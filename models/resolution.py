import datetime

from app import db
from models.user import UserModel


class Resolution(db.Model):
    __tablename__ = "resolutions"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    ended = db.Column(db.Boolean)
    difficulty = db.Column(db.Integer)
    final_time = db.Column(db.INTEGER)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'),
                            nullable=False)

    @staticmethod
    def to_json_date(obj):
        return {
            '__type__': 'datetime',
            'year': obj.year,
            'month': obj.month,
            'day': obj.day,
            'hour': obj.hour,
            'minute': obj.minute,
            'second': obj.second,
            'microsecond': obj.microsecond,
        }

    @staticmethod
    def to_json(x, user=None):

        return {
            'id': x.id,
            'start_date': Resolution.to_json_date(x.start_date),
            'end_date': Resolution.to_json_date(x.end_date),
            'ended': x.ended,
            'difficulty': x.difficulty,
            'final_time': x.final_time,
            'user_id': x.user_id,
            'exercise_id': x.exercise_id,
            "user": user.name if user is not None else ""
        }

    @classmethod
    def end_resolution(cls, resolution_id, penalization):
        current = cls.query.filter_by(id=resolution_id).first()
        if current.ended is True:
            return False
        current.ended = True
        current.end_date = datetime.datetime.now()
        current.final_time = ((current.end_date - current.start_date).total_seconds() + penalization * 10)
        db.session.commit()
        return current

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {"message": "{} row(s) deleted".format(num_rows_deleted)}
        except:
            return {"message": "Something went wrong"}

    @classmethod
    def get_all_my_resolutions(cls, user_id, exercise_list):
        resolutions = []
        for exercise in exercise_list:
            resolutions.append(
                {"exercise": exercise,
                 "resolutions":
                     list(
                         map(lambda x: cls.to_json(x, None),
                             cls.query.filter_by(user_id=user_id, exercise_id=exercise["id"]).order_by(
                                 Resolution.final_time).all()))})

        return resolutions

    @classmethod
    def get_best_times_at_exercise(cls, exercise_id):
        return list(map(lambda x:
                        cls.to_json(x, UserModel.find_by_id(x.user_id)),
                        cls.query.filter_by(exercise_id=exercise_id).order_by(Resolution.final_time).limit(20).all()))
