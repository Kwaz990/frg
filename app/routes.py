from flask import render_template, flash, redirect, url_for, request, Flask, make_response, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Person
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
import os, math, json
from time import time
from datetime import datetime
from random import random
from marshmallow import Schema, fields, pprint, ValidationError



user_id_dict = {
    "1": "Kwasi",
    '2': "Gene",
    '3': "Carter",
    '4': "Kenso"
}


@app.route('/')
@app.route('/index')
@login_required
def index(chartID = 'chart_ID', chartID2 = 'chart_ID2', chartID3 = 'chart_ID3', chartID4 = 'chart_ID4', chart_type = 'pie', chart_height = '100%'):
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

    #The following code queries the db and sets piechart parameters
    #Much of the following code will be repeated for each of the four users
    #being displayed on the index


    emotionDict = {1: 'sad', 2:'neutral', 3: 'happy'}


    ###################################################
    #code for user 1
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    person = Person.query.filter_by(user_id=1).filter(Person.mood)
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    #pprint(result.data)
    result_data = result.data
    pieList = []
    pieDict = {}
    pieMaster = []
    userEmo = []
    pieEmoSum = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data:
        #print(i['mood'])
        pieList.append(i['mood'])
    #print('pieList:', pieList)
    for i in pieList:
        if i in emotionDict:
            userEmo.append(emotionDict[i])
            pieEmoSum[emotionDict[i]] +=1
    #print('userEmo:', userEmo)
    #print('pieEmoSum:', pieEmoSum)
    pieMaster = [{'y':v, 'name': k} for k, v in pieEmoSum.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    #print('pieMaster:', pieMaster)
    
    
    series = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': pieMaster
    }]

    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}


    params = {'chartID': chartID, 'chart':chart, 'series':series, 'title':title, 'xAxis':xAxis, 'yAxis':yAxis}
    chartParams =[params]


    ###################################################
    #code for user 2
    chart2 = {"renderTo": chartID2, "type": chart_type, "height": chart_height}
    person2 = Person.query.filter_by(user_id=2).filter(Person.mood)
    schema = PersonSchema(many=True)
    result2 = schema.dump(person2)
    #pprint(result.data)
    result_data2 = result2.data
    pieList2 = []
    pieDict2 = {}
    pieMaster2 = []
    userEmo2 = []
    pieEmoSum2 = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data2:
        #print(i['mood'])
        pieList2.append(i['mood'])
    #print('pieList:', pieList)
    for i in pieList2:
        if i in emotionDict:
            userEmo2.append(emotionDict[i])
            pieEmoSum2[emotionDict[i]] +=1
    #print('userEmo:', userEmo)
    #print('pieEmoSum:', pieEmoSum)
    pieMaster2 = [{'y':v, 'name': k} for k, v in pieEmoSum2.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    #print('pieMaster:', pieMaster)
    
    
    series2 = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': pieMaster2
    }]

    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}


    params2 = {'chartID2': chartID2, 'chart':chart2, 'series':series2, 'title':title, 'xAxis':xAxis, 'yAxis':yAxis}
    chartParams2 =[params2]


    ####################################################
    #code for user 3

    chart3 = {"renderTo": chartID3, "type": chart_type, "height": chart_height}
    person3 = Person.query.filter_by(user_id=3).filter(Person.mood)
    schema = PersonSchema(many=True)
    result3 = schema.dump(person3)
    #pprint(result.data)
    result_data3 = result3.data
    pieList3 = []
    pieDict3 = {}
    pieMaster3 = []
    userEmo3 = []
    pieEmoSum3 = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data3:
        #print(i['mood'])
        pieList3.append(i['mood'])
    #print('pieList:', pieList)
    for i in pieList3:
        if i in emotionDict:
            userEmo3.append(emotionDict[i])
            pieEmoSum3[emotionDict[i]] +=1
    #print('userEmo:', userEmo)
    #print('pieEmoSum:', pieEmoSum)
    pieMaster3 = [{'y':v, 'name': k} for k, v in pieEmoSum3.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    #print('pieMaster:', pieMaster)
    
    
    series3 = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': pieMaster3
    }]

    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}


    params3 = {'chartID3': chartID3, 'chart':chart3, 'series':series3, 'title':title, 'xAxis':xAxis, 'yAxis':yAxis}
    chartParams3 =[params3]



    ############################################
    #code for user 4

    chart4 = {"renderTo": chartID4, "type": chart_type, "height": chart_height}
    person4 = Person.query.filter_by(user_id=4).filter(Person.mood)
    schema = PersonSchema(many=True)
    result4 = schema.dump(person4)
    #pprint(result.data)
    result_data4 = result4.data
    pieList4 = []
    pieDict4 = {}
    pieMaster4 = []
    userEmo4 = []
    pieEmoSum4 = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data4:
        #print(i['mood'])
        pieList4.append(i['mood'])
    #print('pieList:', pieList)
    for i in pieList4:
        if i in emotionDict:
            userEmo4.append(emotionDict[i])
            pieEmoSum4[emotionDict[i]] +=1
    #print('userEmo:', userEmo)
    #print('pieEmoSum:', pieEmoSum)
    pieMaster4 = [{'y':v, 'name': k} for k, v in pieEmoSum4.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    #print('pieMaster:', pieMaster)
    
    
    series4 = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': pieMaster4
    }]

    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}


    params4 = {'chartID4': chartID4, 'chart':chart4, 'series':series4, 'title':title, 'xAxis':xAxis, 'yAxis':yAxis}
    chartParams4 =[params4]





    return render_template('index.html', title='Home', sat_lev = sat_lev, mood= moodAverage, subjectImg = subjectImg, subjectName = subjectName, impath=impath, chartParams=chartParams, chartParams2=chartParams2, chartParams3=chartParams3, chartParams4=chartParams4)






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



emotionDict = {1: 'sad', 2:'neutral', 3: 'happy'}



#instantiate Marshmallow
#marshmallow is used to serialize sqlalchemy db data into json

class PersonSchema(Schema):
    id = fields.Int()
    timestamp = fields.DateTime()
    mood = fields.Int()
    user_id = fields.Int()



@app.route("/pieData")
def pieData():
    person = Person.query.filter_by(user_id=3).filter(Person.mood)
    #person = Person.query.all()
   # person_dict = person.__dict__
    #del person_dict['']
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    pprint(result.data)
    result_data = result.data
    pieList = []
    pieDict = {}
    pieMaster = []
    userEmo = []
    for i in result_data:
        print(i['mood'])
        pieList.append(i['mood'])
    print('pieList:', pieList)
    for i in pieList:
        if i in emotionDict:
            userEmo.append(emotionDict[i])
            #pieDict[i]=emotionDict[i]
    print('userEmo:', userEmo)
    pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    print('pieMaster:', pieMaster)        

    return jsonify(pieMaster)
    


    '''
    You want pieData in the folllowing form:
    data: [{ y: 1, name: "Point2", color: "#00FF00" }, { y: 7, name: "Point1", color: "#FF00FF" }]

    '''
@app.route('/pie')
def pie(chartID = 'chart_ID', chart_type = 'pie', chart_height = '100%'):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    person = Person.query.filter_by(user_id=3).filter(Person.mood)
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    pprint(result.data)
    result_data = result.data
    pieList = []
    pieDict = {}
    pieMaster = []
    userEmo = []
    pieEmoSum = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data:
        print(i['mood'])
        pieList.append(i['mood'])
    print('pieList:', pieList)
    for i in pieList:
        if i in emotionDict:
            userEmo.append(emotionDict[i])
            pieEmoSum[emotionDict[i]] +=1
    print('userEmo:', userEmo)
    print('pieEmoSum:', pieEmoSum)
    pieMaster = [{'y':v, 'name': k} for k, v in pieEmoSum.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    print('pieMaster:', pieMaster)
    
    
    series = [{
        'name': 'Brands',
        'colorByPoint': 'true',
        'data': pieMaster
    }]


    '''
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
    '''

    #series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'Pie Test, Yo!'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    params = {'chartID': chartID, 'chart':chart, 'series':series, 'title':title, 'xAxis':xAxis, 'yAxis':yAxis}
    chartParams =[params]
    


    return render_template('pie.html', chartParams=chartParams)
   # return render_template('pie.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



@app.route('/subject/<user_id>')
@login_required
def subject(user_id, chartID = 'chart_ID', chart_type = 'line', chart_height = '100%'):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    person = Person.query.filter_by(user_id=user_id).filter(Person.mood)
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    #pprint(result.data)
    result_data = result.data
    mood = []
    for i in result_data:
        mood.append(i['mood'])
    print('mood:', mood)   

    pointStart = Person.query.filter_by(user_id=3).filter(Person.timestamp)
    pointStartSchema = PersonSchema(many=True)
    pointStartResult = pointStartSchema.dump(pointStart)
    #pprint(pointStartResult.data)
    pointStartData = pointStartResult.data
    #the datetime data has a T in the formatting. The following code correctly
    #formatts the datetime data to be used as highcharts data
    time = []
    dateAndTime = []
    dateTime_almost = []
    dateTime_formatted = []
    for i in pointStartData:
       # dateAndTime.append(i['timestamp'])
        time.append(i['timestamp'])
    for i in time:
        dateAndTime.append(i.split('T'))
    for i in dateAndTime:
        dateTime_almost.append(' '.join(i))
    for i in dateTime_almost:
        dateTime_formatted.append(i[:19])
 #   print('intermediate', dateAndTime)
  #  print('******************************')
   # print('almost', dateTime_almost)
    #print('###########################')
    #print('formatted', dateTime_formatted)
    #print('time:', time)
    #print('time[0]:',time[0])

    series = [{
        'data': mood
    },
        {
    'pointStart': dateTime_formatted 
    }]

    #plotOptions does not seem to work in python implementation
    plotOptions = {
    'series': {
      'pointStart': dateTime_formatted[0]  #datetime.strptime(dateTime_formatted[0], '%Y-%m-%d %H:%M:%S')
    }
  }


    title = {"text": 'ChartDemo, Yo!'}
    xAxis = {"title": {'text': 'Time'}}
    yAxis = {"title": {"text": 'Emotion Integer'}}

    return render_template('subjectDetails.html', title= title, chartID=chartID, chart=chart, series=series, xAxis=xAxis, yAxis=yAxis, user_id=user_id)# plotOptions = plotOptions)


@app.route('/liveEmo')
@login_required
def liveEmo():
    person = Person.query.filter_by(user_id=3).filter(Person.mood)
    schema = PersonSchema(many=True)
    result = schema.dump(person)
    pprint(result.data)
    result_data = result.data
    pieList = []
    pieDict = {}
    pieMaster = []
    userEmo = []
    pieEmoSum = {'sad': 0, 'neutral': 0, 'happy': 0}
    for i in result_data:
        print(i['mood'])
        pieList.append(i['mood'])
    print('pieList:', pieList)
    for i in pieList:
        if i in emotionDict:
            userEmo.append(emotionDict[i])
            pieEmoSum[emotionDict[i]] +=1
    print('userEmo:', userEmo)
    print('pieEmoSum:', pieEmoSum)
    pieMaster = [{'y':v, 'name': k} for k, v in pieEmoSum.items()]
    #pieMaster = [{'y':k, 'name': v} for k, v in zip(pieList, userEmo)]
    print('pieMaster:', pieMaster)
    return jsonify(pieMaster)



@app.route('/live-data')
@login_required
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response