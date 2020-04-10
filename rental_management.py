from flask import Flask, render_template, url_for
from database_setup import Property, Tenant, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///rentalmanagement.db')
Base.metadata.bind = engine


@app.route('/')
@app.route('/home/')
def home():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    properties = session.query(Property).all()
    tenants = session.query(Tenant).all()
    return render_template('homepage.html', properties=properties, tenants=tenants)


@app.route('/properties/')
def showProperties():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    properties = session.query(Property).all()
    tenants = session.query(Tenant).all()
    return render_template("properties.html", properties=properties)


@app.route('/tenants/')
def showTenants():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    tenants = session.query(Tenant).all()
    return render_template("tenants.html", tenants=tenants)


@app.route('/property/<int:property_id>/')
def showProperty(property_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    property = session.query(Property).filter_by(id=property_id).one()
    return render_template("property.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
