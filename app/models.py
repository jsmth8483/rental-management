from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), index=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(250), index=True, nullable=False)
    phone = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }
    
class Tenant(User):
    __tablename__ = 'tenant'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))    

    __mapper_args__ = {
        'polymorphic_identity' :'tenant'
    }

class PropertyManager(User):
    __tablename__ = 'property_manager'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    properties = db.relationship('Property', backref=db.backref('property_manager', lazy='joined'))
    __mapper_args__ = {
        'polymorphic_identity' :'property_manager'
    }

class Landlord(User):
    __tablename__ = 'landlord'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    properties = db.relationship('Property', backref=db.backref('landlord', lazy='joined'))
    __mapper_args__ = {
        'polymorphic_identity' :'landlord'
    }


class Property(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    streetAddress = db.Column(db.String(250), nullable=False)
    unitNumber = db.Column(db.String(250))
    city = db.Column(db.String(250), nullable=False)
    zipCode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(250))
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('property_manager.id'))
    
    tenants = db.relationship('Tenant', backref=db.backref('property', lazy='joined'))


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)