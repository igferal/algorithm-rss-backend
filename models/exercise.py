from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    subtitle = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    pseudocode = db.Column(db.String(5000), nullable=False)
    children = relationship("Heuristic")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def return_all(cls):
        def to_json(ex):
            heuristics = list(
                map(
                    lambda h: {"description": h.description, "rate": h.rate},
                    ex.children,
                )
            )

            return {
                "id": ex.id,
                "type": ex.type,
                "name": ex.name,
                "description": ex.description,
                "pseudocode": ex.pseudocode,
                "image": ex.image,
                "subtitle": ex.subtitle,
                "heuristics": heuristics
            }

        return {"exercises": list(map(lambda x: to_json(x), Exercise.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {"message": "{} row(s) deleted".format(num_rows_deleted)}
        except:
            return {"message": "Something went wrong"}


class Heuristic(db.Model):
    __tablename__ = "heuristic"
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, ForeignKey("exercises.id"))
    description = db.Column(db.String(120), nullable=False)
    rate = db.Column(db.Integer(), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(name=username).first()
