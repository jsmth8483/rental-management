from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask import current_app as app
from .models import db, Property, Tenant, User, PropertyManager, Landlord
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/home/')
@login_required
def home() -> 'html':
    
    properties = Property.query.filter_by(landlord_id=current_user.id)
    tenants = Tenant.query.all()
    users = User.query.all()
    return render_template('homepage.html', properties=properties, tenants=tenants)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/properties/')
@login_required
def showProperties() -> 'html':
    properties = Property.query.all()
    tenants = Tenant.query.all()
    return render_template("properties.html", properties=properties)


@app.route('/tenants/')
@login_required
def showTenants() -> 'html':
    tenants = Tenant.query.all()
    return render_template("tenants.html", tenants=tenants)


@app.route('/property/<int:property_id>/')
@login_required
def propertyDetails(property_id: int) -> 'html':
    property = Property.query.filter_by(id=property_id).one()
    tenants = Tenant.query.filter_by(property_id=property_id).all()
    return render_template("property.html", property=property, tenants=tenants)


@app.route('/property/new/', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def newTenant(property_id: int) -> 'html':
    property = Property.query.filter_by(id=property_id).one()
    if request.method == 'POST':
        newTenant = Tenant(
            first_name=request.form['first_name'], last_name=request.form['last_name'], phone=request.form['phone'], email=request.form['email'], property_id=property_id)
        db.session.add(newTenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=property_id))
    return render_template('newTenant.html', property=property)


@app.route('/tenant/<int:tenant_id>/edit/', methods=['GET', 'POST'])
@login_required
def editTenant(tenant_id: int) -> 'html':
    tenant = Tenant.query.filter_by(id=tenant_id).one()
    if request.method == 'POST':
        tenant.first_name = request.form['first_name']
        tenant.last_name = request.form['last_name']
        tenant.phone = request.form['phone']
        tenant.email = request.form['email']
        db.session.add(tenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property.id))
    return render_template('editTenant.html', tenant=tenant)


@app.route('/property/<int:property_id>/delete/', methods=['GET', 'POST'])
@login_required
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
@login_required
def deleteTenant(tenant_id: int) -> 'html':
    tenant = Tenant.query.filter_by(id=tenant_id).one()
    streetAddress = tenant.property.streetAddress
    if request.method == 'POST':
        db.session.delete(tenant)
        db.session.commit()
        return redirect(url_for('propertyDetails', property_id=tenant.property_id))
    return render_template('deleteTenant.html', tenant=tenant, streetAddress=streetAddress)

