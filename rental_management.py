from flask import Flask, render_template, url_for
from database_setup import Property, Tenant, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///rentalmanagement.db')
Base.metadata.bind = engine


@app.route('/')
@app.route('/home')
def home():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    properties = session.query(Property).all()
    tenants = session.query(Tenant).all()
    return render_template('homepage.html', properties=properties, tenants=tenants)


@app.route('/properties')
def showProperties():
    return render_template("properties.html")


@app.route('/tenants')
def showTenants():
    return render_template("tenants.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
