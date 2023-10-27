from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'

    serialize_rules = ('-owner.pets',)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('owners.id'))

    owner = db.relationship('Owner', back_populates='pets')  ####

    @validates('name')
    def validate_name(self, key, new_name):
        if len(new_name) == 0:
            raise ValueError('name must be at least one char')
        else:
            return new_name  # this value gets set as the name

    def __repr__(self):
        return f"<Pet {self.name}>"

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'

    serialize_rules = ('-pets.owner',)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    pets = db.relationship('Pet', back_populates='owner', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Owner {self.name}>"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, new_pass):
        pass_hash = bcrypt.generate_password_hash(new_pass.encode('utf-8'))
        self._password_hash = pass_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, 
            password.encode('utf-8')
        )
