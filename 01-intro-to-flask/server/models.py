from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'

    serialize_rules = ('-owner.pets',)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('owners.id'))

    owner = db.relationship('Owner', back_populates='pets')  ####

    def __repr__(self):
        return f"<Pet {self.name}>"

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'

    serialize_rules = ('-pets.owner',)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    pets = db.relationship('Pet', back_populates='owner')  #####

    def __repr__(self):
        return f"<Owner {self.name}>"
