import datetime

from app import db


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
    def to_json(x):
        return {
            'id': x.id,
            'start_date': Resolution.to_json_date(x.start_date),
            'end_date': Resolution.to_json_date(x.end_date),
            'ended': x.ended,
            'difficulty': x.difficulty,
            'final_time': x.final_time,
            'user_id': x.user_id,
            'exercise_id': x.exercise_id
        }

    @classmethod
    def end_resolution(cls, resolution_id):
        current = cls.query.filter_by(id=resolution_id).first()
        if current.ended is True:
            return False
        current.ended = True
        current.end_date = datetime.datetime.now()
        current.final_time = (current.end_date - current.start_date).total_seconds()
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
