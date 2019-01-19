from time import time
from random import random, randint
from app import app, db, login
from datetime import datetime, timedelta
from app.models import Person, User



dbFile = 'app.db'


timestamp_begin = datetime(2019, 1,1)  # 01/01/14 00:00
#timestamp_end = timestamp_begin +  60*100
timestamp_end = datetime(2019,1,16)
pitch = timedelta(days=1)

#parameters are timestamp mood user id


# function to commit facial expression integer (a 1-5 integer) and boolean for face detected.
def commitFacialData(mood, timestamp, user_id):
    #connection, cursor = connect()
    mood = mood
    time = timestamp
    user_id = 2
    newFacialData = Person(timestamp=time, mood= mood, user_id=4)
    db.session.add(newFacialData)
    db.session.commit()
    print(True)
    return True

mood = randint(0, 3)    
timestamp = timestamp_begin

while timestamp <= timestamp_end:
    commitFacialData(mood, timestamp, user_id=3)
    timestamp += pitch
    mood = randint(1,3)
    print("Iterations left :", (timestamp_end-timestamp)/pitch)



'''
    # if 1 or more faces are detected make a db commit with boolean value and ineger value for facial expression
    if len(faces) > 0:
            facesBoolean = True
            expressionInteger = moodrating
            commitFacialData(facesBoolean, expressionInteger, timeStamp)
'''