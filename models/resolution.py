from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Resolution(db.Model):
    __tablename__ = "resolutions"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    difficulty = db.Column(db.Integer)
    final_time = db.Column(db.DATETIME)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'),
                          nullable=False)


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
