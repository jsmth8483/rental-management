from flask import Flask, render_template, url_for, request, redirect
from flask import current_app as app
from .models import db, Property, Tenant

@app.route('/')
@app.route('/home/')
def home() -> 'html':
    
    properties = Property.query.all()
    tenants = Tenant.query.all()
    return render_template('homepage.html', properties=properties, tenants=tenants)


@app.route('/properties/')
def showProperties() -> 'html':
    
    properties = Property.query.all()
    tenants = Tenant.query.all()
    return render_template("properties.html", properties=properties)


@app.route('/tenants/')
def showTenants() -> 'html':

    tenants = Tenant.query.all()
    return render_template("tenants.html", tenants=tenants)


@app.route('/property/<int:property_id>/')
def propertyDetails(property_id: int) -> 'html':

    property = Property.query.filter_by(id=property_id).one()
    tenants = Tenant.query.filter_by(property_id=property_id).all()
    return render_template("property.html", property=property, tenants=tenants)


@app.route('/property/new/', methods=['GET', 'POST'])
def newProperty() -> 'html':
    if request.method == 'POST':
        
        newProperty = Property(
            title=request.form['title'], streetAddress=request.form['streetAddress'], unitNumber=request.form['unitNumber'],
            city=request.form['city'], zipCode=request.form['zipCode'], state=request.form['state'])
        db.session.add(newProperty)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=newProperty.id))
    return render_template('newProperty.html')


@app.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
def editProperty(property_id: int) -> 'html':
    
    property = Property.query.filter_by(id=property_id).one()
    if request.method == 'POST':
        property.title = request.form['title']
        property.streetAddress = request.form['streetAddress']
        property.unitNumber = request.form['unitNumber']
        property.city = request.form['city']
        property.zipCode = request.form['zipCode']
        property.state = request.form['state']
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('editProperty.html', property=property)


@app.route('/property/<int:property_id>/tenants/new/', methods=['GET', 'POST'])
def newTenant(property_id: int) -> 'html':
    
    property = Property.query.filter_by(id=property_id).one()
    if request.method == 'POST':
        newTenant = Tenant(
            name=request.form['name'], phone=request.form['phone'], email=request.form['email'], property_id=property_id)
        db.session.add(newTenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('newTenant.html', property=property)


@app.route('/tenant/<int:tenant_id>/edit/', methods=['GET', 'POST'])
def editTenant(tenant_id: int) -> 'html':
    
    tenant = Tenant.query.filter_by(id=tenant_id).one()
    if request.method == 'POST':
        tenant.name = request.form['name']
        tenant.phone = request.form['phone']
        tenant.email = request.form['email']
        db.session.add(tenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property.id))
    return render_template('editTenant.html', tenant=tenant)


@app.route('/property/<int:property_id>/delete/', methods=['GET', 'POST'])
def deleteProperty(property_id: int) -> 'html':
    
    property = Property.query.filter_by(id=property_id).one()
    if request.method == 'POST':
        tenants = Tenant.query.filter_by(
            property_id=property_id).all()
        for tenant in tenants:
            db.session.delete(tenant)
        db.session.delete(property)
        db.session.commit()
        return redirect(url_for('showProperties'))

    return render_template('deleteProperty.html', property=property)


@app.route('/tenant/<int:tenant_id>/delete/', methods=['GET', 'POST'])
def deleteTenant(tenant_id: int) -> 'html':
    
    tenant = Tenant.query.filter_by(id=tenant_id).one()
    streetAddress = tenant.property.streetAddress
    if request.method == 'POST':
        db.session.delete(tenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property_id))
    return render_template('deleteTenant.html', tenant=tenant, streetAddress=streetAddress)
