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
            title=request.form['title'], streetAddress=request.form['streetAddress'], unitNumber=request.form['unitNumber'],
            city=request.form['city'], zipCode=request.form['zipCode'], state=request.form['state'])
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
        property.title = request.form['title']
        property.streetAddress = request.form['streetAddress']
        property.unitNumber = request.form['unitNumber']
        property.city = request.form['city']
        property.zipCode = request.form['zipCode']
        property.state = request.form['state']
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
            name=request.form['name'], phone=request.form['phone'], email=request.form['email'], property_id=property_id)
        session.add(newTenant)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('newTenant.html', property=property)


@app.route('/tenant/<int:tenant_id>/edit/', methods=['GET', 'POST'])
def editTenant(tenant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    tenant = session.query(Tenant).filter_by(id=tenant_id).one()
    if request.method == 'POST':
        tenant.name = request.form['name']
        tenant.phone = request.form['phone']
        tenant.email = request.form['email']
        session.add(tenant)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property.id))
    return render_template('editTenant.html', tenant=tenant)


@app.route('/tenant/<int:tenant_id>/delete/', methods=['GET', 'POST'])
def deleteTenant(tenant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    tenant = session.query(Tenant).filter_by(id=tenant_id).one()
    streetAddress = tenant.property.streetAddress
    if request.method == 'POST':
        session.delete(tenant)
        session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property_id))
    return render_template('deleteTenant.html', tenant=tenant, streetAddress=streetAddress)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
