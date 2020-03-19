from sqlalchemy.ext.hybrid import hybrid_property


from application import db
from base.base_models import BaseModel
from helper.helper import flatten


class Person(BaseModel):

    person_id = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    live = db.Column(db.Boolean, default=True)
    # __table_args__ = (db.UniqueConstraint('firstname', 'birthdate', name='_firstname_birthday_uc'),)

    # did not use backref as I like auto-complete
    parents = db.relationship(
        "Person",
        secondary="relation",
        primaryjoin="Person.id==relation.c.parent_id",
        secondaryjoin="Person.id==relation.c.child_id",
        lazy="joined",
    )
    children = db.relationship(
        "Person",
        secondary="relation",
        primaryjoin="Person.id==relation.c.child_id",
        secondaryjoin="Person.id==relation.c.parent_id",
        lazy="joined",
    )

    @hybrid_property
    def siblings(self):
        return flatten([parent.children for parent in self.parents])

    @hybrid_property
    def grandparents(self):
        return flatten([parent.parents for parent in self.parents])

    @hybrid_property
    def grandchildren(self):
        return flatten([child.children for child in self.children])

    @hybrid_property
    def cousins(self):
        two_generations_up = flatten([parent.parents for parent in self.parents])
        aunts_uncles = set(flatten([person.children for person in two_generations_up])) - set(self.parents)
        return flatten([person.children for person in aunts_uncles])

    @classmethod
    def find_by_id(cls, person_id):
        return cls.query.filter_by(person_id=person_id, live=True).first()

    @classmethod
    def get_all(cls, limit=10):
        return cls.query.limit(limit).all()

    @classmethod
    def get_all_live(cls):
        return cls.query.filter_by(live=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Relation(BaseModel):

    parent_id = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="CASCADE"))
    child_id = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="CASCADE"))
