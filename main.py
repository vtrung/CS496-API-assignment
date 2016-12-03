# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]

import logging
import time
import pprint
import json
from data.modelndb import *
from data.crudndb import *

# [START imports]
from flask import Flask, render_template, request, redirect, url_for, jsonify
# [END imports]

from google.appengine.ext import ndb

app = Flask(__name__)


### ----------- API ------- ####
## API - PERSON ##
# get all person
@app.route('/api/person', methods=['GET'])
def apiGetAllPerson():
    query = Person.query()
    return json.dumps([p.to_dict() for p in query.fetch()])

# get single person by username
@app.route('/api/person/<username>', methods=['GET'])
def apiGetPerson(username):
    person = GetPerson(username)
    if person:
        return json.dumps(person.to_dict())
    return "failed"

# create person
@app.route('/api/person', methods=['POST'])
def apiCreatePerson():
    try:
        person = CreatePerson(request.form['username'], request.form['password'])
        return json.dumps(person.to_dict())
    except:
        return "failed"

# delete person
@app.route('/api/person/<username>', methods=['DELETE'])
def apiDeletePerson(username):
    try:
        result = DeletePerson(username)
        if result is None:
            return "success"
        return "failed"
    except:
        return "failed"

@app.route('/api/verify', methods=['POST'])
def apiVerifyPerson():
    try:
        person = VerifyPerson(request.form.get('username'), request.form.get('password'))
        return json.dumps(person.to_dict())
    except:
        return "failed"


### API-EVENTS ###


# get all events
@app.route('/api/event', methods=['GET'])
def apiGetEvents():
    return json.dumps([p.to_dict() for p in GetEvents().fetch()])

# get an event
@app.route('/api/event/<name>', methods=['GET'])
def apiGetEvent(name):
    event = GetEvent(name)
    if event:
        return json.dumps(event.to_dict())
    return "failed"

# create an event
@app.route('/api/event', methods=['POST'])
def apiCreateEvent():
    try:
        print "TEST CreateEvent"
        a = CreateEvent(request.form['name'] , request.form['time'] , request.form['loc'] , request.form['des'])
        return json.dumps(a.to_dict())
    except:
        return "failed"

# update an event
@app.route('/api/event/<name>', methods=['PUT'])
def apiUpdateEvent(name):
    try:
        event = UpdateEvent(name, request.form['time'], request.form['loc'], request.form['des'])
        return "success"
    except:
        return "failed"

# delete an event
@app.route('/api/event/<name>', methods=['DELETE'])
def apiDeleteEvent(name):
    try:
        result = DeleteEvent(name)
        if result is None:
            return "success"
        return "failed"
    except:
        return "failed"

@app.route('/api/eventperson', methods=['POST'])
def apiCreateEventPerson():
    try:
        print "TEST CreateEvent"
        a = CreateEventPerson(request.form['username'], request.form['name'] , request.form['time'] , request.form['loc'] , request.form['des'])
        return json.dumps(a.to_dict())
    except:
        return "failed"


@app.route('/api/addperson/<event>', methods=['POST'])
def apiAddEventPerson(event):
    try:
        result = AddEventPerson(request.form['user'], event)
        return "success"
    except:
        return "false"

@app.route('/api/addperson/<event>/<user>', methods=['DELETE'])
def apiDeleteEventPerson(event, user):
    try:
        DeleteEventPerson(user, event)
        return "success"
    except:
        return "false"


### API-GAME ###

# get games by event
@app.route('/api/game/<event>', methods=['GET'])
def apiGetGames(event):
    return json.dumps([p.to_dict() for p in GetGames(event)])

# get game
@app.route('/api/game/<event>/<name>', methods=['GET'])
def apiGetGame(event, name):
    game = GetGame(event, name)
    if game:
        return json.dumps(game.to_dict())
    return "failed"

# create game
@app.route('/api/game', methods=['POST'])
def apiCreateGame():
    try:
        game = CreateGame(request.form['event'], request.form['name'], request.form['description'])
        return json.dumps(game.to_dict())
    except:
        return "failed"

# update game
@app.route('/api/game/<event>/<name>', methods=['PUT'])
def apiUpdateGame(event, name):
    try:
        print request.form['description']
        game = UpdateGame(event, name, request.form['description'])
        return json.dumps(game.to_dict())
    except:
        return "failed"

# delete game
@app.route('/api/game/<event>/<name>', methods=['DELETE'])
def apiDeleteGame(event, name):
    try:
        result = DeleteGame(event, name)
        if result is None:
            return "success"
        return "failed"
    except:
        return "failed"

### END API ###



###### SINGLE PAGE APPLICATION ######

@app.route('/')
def index():
    webstring = "Ving Trung CS496 Fall 2016: \n"
    webstring = webstring + 'Current Time: ' + str(time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)'))
    query = User.query()
    for user in query:
         print user.key.urlsafe()
    return render_template(
        'index.html',
        webstring=webstring,
        query=query)

@app.route('/userformsubmit', methods=['POST'])
def userformsubmit():
    user = User(name=request.form['name'])
    user.birthdate = request.form['bday']
    user.skill = int(request.form['skill'])
    user.gender = request.form['gender']
    if request.form.get("teacher"):
        user.teacher = True
    if request.form.get("student"):
        user.student = True
    if request.form.get("ta"):
        user.ta = True
    user.put()
    webstring = "Added: " + request.form['name']
    return render_template('message.html', webstring=webstring)

@app.route('/userformsubmit', methods=['GET'])
def userformsubmitget():
    return redirect(url_for('index'))

### DELETING
@app.route('/userformdelete', methods=['POST'])
def userformdelete():
    key = request.form['key']
    ndb.Key(urlsafe=key).delete()
    webstring = "Deleted: " + request.form['key']
    return render_template('message.html', webstring=webstring)

@app.route('/userformdelete', methods=['GET'])
def userformdeleteget():
    return redirect(url_for('index'))


@app.route('/userupdate')
def userupdate():
    user = request.args.get('user')
    if not user:
        return redirect(url_for('index'))
    u = ndb.Key(urlsafe=user).get()
    return render_template(
        'user_update.html',
        user=u,
        key=user)


@app.route('/userformupdate', methods=['POST'])
def userformupdate():
    key = request.form['key']
    #a = eval(str(key))
    user = ndb.Key(urlsafe=key).get()
    user.birthdate = request.form['bday']
    user.skill = int(request.form['skill'])
    user.gender = request.form['gender']
    if request.form.get("teacher"):
        user.teacher = True
    if request.form.get("student"):
        user.student = True
    if request.form.get("ta"):
        user.ta = True
    user.put()
    webstring = "Updated: " + request.form['name']
    return render_template('message.html', webstring=webstring)

@app.route('/userformupdate', methods=['GET'])
def userformupdateget():
    return redirect(url_for('index'))

# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]

# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)

###### END SINGLE PAGE ######

@app.errorhandler(405)
def post_error():
    return redirect(url_for('index'))


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
