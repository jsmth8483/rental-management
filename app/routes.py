from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask import current_app as app
from .models import db, Property, Tenant
from app.forms.login_form import LoginForm
from app.login import is_logged_in

@app.route('/')
@app.route('/home/')
@is_logged_in
def home() -> 'html':
    
    properties = Property.query.all()
    tenants = Tenant.query.all()
    return render_template('homepage.html', properties=properties, tenants=tenants)
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        flash('Welcome, {}'.format(form.username.data))
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/properties/')
@is_logged_in
def showProperties() -> 'html':
    properties = Property.query.all()
    tenants = Tenant.query.all()
    return render_template("properties.html", properties=properties)


@app.route('/tenants/')
@is_logged_in
def showTenants() -> 'html':
    tenants = Tenant.query.all()
    return render_template("tenants.html", tenants=tenants)


@app.route('/property/<int:property_id>/')
@is_logged_in
def propertyDetails(property_id: int) -> 'html':
    property = Property.query.filter_by(id=property_id).one()
    tenants = Tenant.query.filter_by(property_id=property_id).all()
    return render_template("property.html", property=property, tenants=tenants)


@app.route('/property/new/', methods=['GET', 'POST'])
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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
@is_logged_in
def deleteTenant(tenant_id: int) -> 'html':
    tenant = Tenant.query.filter_by(id=tenant_id).one()
    streetAddress = tenant.property.streetAddress
    if request.method == 'POST':
        db.session.delete(tenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property_id))
    return render_template('deleteTenant.html', tenant=tenant, streetAddress=streetAddress)
