from flask import render_template, flash, redirect, url_for, request, Flask, make_response, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Person
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
import os, math, json
from time import time
from random import random
from marshmallow import Schema, fields, pprint, ValidationError








user_id_dict = {
    "1": "Kwasi",
    '2': "Gene",
    '3': "Carter",
    '4': "Kenso"
}


user_id_dict = {
    "1": "Kwasi",
    '2': "Gene",
    '3': "Carter",
    '4': "Kenso"
}


@app.route('/')
@app.route('/index')
@login_required
def index():
    #user = {'username': 'Miguel'}
    sat_lev = { 
        'one': "angry"
        }

    moodQuery=Person.query.filter_by(user_id=1).all()
    moodSum = 0
    moodAverage = 0
    subjectId = moodQuery
    subjectName = 'Kwasi'
    subjectImg = 'default'
    #if len(moodQuery) > 0:
    #    subjectName = user_id_dict[moodQuery[0]]

        #To check if folder exists, create if doesnt exists
    exist_path = os.path.join('snapShots', subjectName)
    if os.path.exists(exist_path):
        subjectImg = os.path.join('snapShots', subjectName, '{}.jpg'.format(subjectName))
    else:
        os.makedirs(os.path.join('snapShots', subjectName))

    for i in range(len(moodQuery)):
        moodSum += moodQuery[i].mood
        moodAverage += (moodSum/(len(moodQuery)))
        moodAverage = math.ceil(moodAverage)
    impath = "/static/snapShots/{}/{}.jpg".format(subjectName, subjectName)

    return render_template('index.html', title='Home', sat_lev = sat_lev, mood= moodAverage, subjectImg = subjectImg, subjectName = subjectName, impath=impath)






@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                            title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#instantiate Marshmallow
#ma = Marshmallow(app)

class PersonSchema(Schema):
    id = fields.Int()
    timestamp = fields.DateTime()
    mood = fields.Int()
    user_id = fields.Int()



@app.route("/data.json")
def data():
   # person = Person.query.filter_by(user_id=2) #filter_by(user_id=2)
    person = Person.query.all()
   # person_dict = person.__dict__
    #del person_dict['']
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    pprint(result.data)
    return jsonify({'person': result.data})
    
    #return json.dumps(person)



@app.route('/pie')
def pie(chartID = 'chart_ID', chart_type = 'pie', chart_height = '100%'):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': [{
            'name': 'Chrome',
            'y': 61.41,
            'sliced': 'true',
            'selected': 'true'
        }, {
            'name': 'Internet Explorer',
            'y': 11.84
        }, {
            'name': 'Firefox',
            'y': 10.85
        }, {
            'name': 'Edge',
            'y': 4.67
        }, {
            'name': 'Safari',
            'y': 4.18
        }, {
            'name': 'Sogou Explorer',
            'y': 1.64
        }, {
            'name': 'Opera',
            'y': 1.6
        }, {
            'name': 'QQ',
            'y': 1.2
        }, {
            'name': 'Other',
            'y': 2.61
        }]
    }]

    #series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('pie.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



#TODO: make this function link to the live graph page
@app.route('/subject/<subjectName>', methods=['GET', 'POST'])
@login_required
def subject(subjectName):
    pass
    return render_template('subjectDetails.html', title= 'Spying on <subjectName>', subjectName=subjectName, data='test')

@app.route('/live-data')
@login_required
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response