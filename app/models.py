from . import db

class Property(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    streetAddress = db.Column(db.String(250), nullable=False)
    unitNumber = db.Column(db.String(250))
    city = db.Column(db.String(250), nullable=False)
    zipCode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(250))

class Tenant(db.Model):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(250), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property = db.relationship('Property', backref=db.backref('tenant', lazy=True))