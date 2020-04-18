from flask import Flask, render_template, url_for, request, redirect
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
def propertyDetails(property_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    property = session.query(Property).filter_by(id=property_id).one()
    tenants = session.query(Tenant).filter_by(property_id=property_id).all()
    return render_template("property.html", property=property, tenants=tenants)


@app.route('/property/new/', methods=['GET', 'POST'])
def newProperty():
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        newProperty = Property(
            nickname=request.form['nickname'], address=request.form['address'])
        session.add(newProperty)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=newProperty.id))
    return render_template('newProperty.html')


@app.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
def editProperty(property_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    property = session.query(Property).filter_by(id=property_id).one()
    if request.method == 'POST':
        property.nickname = request.form['nickname']
        property.address = request.form['address']
        session.add(property)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('editProperty.html', property=property)


@app.route('/property/<int:property_id>/tenants/new/', methods=['GET', 'POST'])
def newTenant(property_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    property = session.query(Property).filter_by(id=property_id).one()
    if request.method == 'POST':
        newTenant = Tenant(
            name=request.form['name'], phone=request.form['phone'], property_id=property_id)
        session.add(newTenant)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('newTenant.html', property=property)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
