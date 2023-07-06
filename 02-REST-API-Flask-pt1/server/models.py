
from flask_sqlalchemy import SQLAlchemy
# 6. ✅ Import `SerializerMixin` from `sqlalchemy_serializer`
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

# 7. ✅ Pass `SerializerMixin` to `Productions`
class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'

    serialize_rules = ('-cast_members.production',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship('CastMember', backref='production')

    @validates('budget')
    def validate_budget(self, key, new_budget):
        if new_budget < 0:
            raise ValueError('budget cannot be negative')
        return new_budget

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'
    
    # def to_dict(self):
    #     """Return the Production obj as a dictionary"""
    #     cast_members = []
    #     for cast in self.cast_members:
    #         cast_members.append(cast.to_dict())
    #     return {
    #         'id': self.id,
    #         'title': self.title,
    #         'genre': self.genre,
    #         'cast_members': cast_members
    #     }

# 8. ✅ Pass `SerializerMixin` to `CastMember`
class CastMember(db.Model, SerializerMixin):
    __tablename__ = 'cast_members'

    serialize_rules = ('-productions.cast_members',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    
    # 8.1 ✅ Create a serialize rule that will help add our `production` to the response.
      
    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'
    
    # def to_dict(self):
    #     return {
    #         'name': self.name
    #     }

 # 9. ✅ Navigate back to `app.py` for further steps.