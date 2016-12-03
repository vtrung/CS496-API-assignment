from modelndb import *

## PERSON QUERY

def PersonExist(username):
    print "Person Exist"
    person = Person.query(Person.Username == username).fetch()
    print person
    if len(person) > 0:
        return person
    return False

def GetPerson(username):
    person = PersonExist(username)
    if not person:
        return False
    return person[0]

def VerifyPerson(username, password):
    person = Person.query(Person.Username == username, Person.Password == password).fetch()
    if len(person) > 0:
        return person[0]
    return False

def CreatePerson(username, password):
    print "test1"
    if PersonExist(username):
        return False
    print "creating person"
    person = Person()
    person.Username = username
    person.Password = password
    print "after age"
    person.put()
    return person

def UpdatePerson(username, name, gender, age):
    result = PersonExist(username)
    if not result:
        return False
    person = result[0]
    person.Name = name
    person.Gender = gender
    person.Age = int(age)
    return person.put()

def DeletePerson(username):
    print "Deleting"
    person = PersonExist(username)
    if not person:
        return False
    p = person[0]
    k = p.put()
    return k.delete()

def GetAllPerson():
    query = Person.query()
    return query

def GetPeopleByEvent():
    query = Team.query()
    return query


## EVENT QUERY
def EventExist(name):
    print "Event Exist"
    event = Event.query(Event.Name == name).fetch()
    print event
    if len(event) > 0:
        return event
    return False

def GetEvents():
    query = Event.query()
    return query

def GetEvent(name):
    event = EventExist(name)
    if not event:
        return False
    return event[0]

def CreateEvent(name, date, location, description):
    print "in CreateEvent"
    if EventExist(name):
        return False
    event = Event()
    event.Name = name
    event.Date = date
    event.Location = location
    event.Description = description
    event.put()
    return event

def DeleteEvent(name):
    event = EventExist(name)
    if not event:
        return False
    e = event[0]
    DeleteGames(e.Name)
    k = e.put()
    return k.delete()


def UpdateEvent(name, date, location, description):
    print "in UpdateEvent"
    result = EventExist(name)
    if not result:
        return False
    print "in UpdateEvent2"
    event = result[0]
    event.Date = date
    event.Location = location
    event.Description = description
    event.put()
    print "in UpdateEvent3"
    return event

## GAME QUERY
def GameExist(event, name):
    print "Game Exist"
    game = Game.query(Game.Name == name, Game.Event == event).fetch()
    if len(game) > 0:
        print "game exist"
        return game
    print "game does not exist"
    return False

def GetGames(event):
    query = Game.query(Game.Event == event).fetch()
    return query

def GetGame(event, name):
    game = GameExist(event, name)
    if not game:
        return False
    return game[0]

def CreateGame(event, name, description):
    if not EventExist(event):
        return False
    if GameExist(event, name):
        return False
    print "creating game"
    game = Game()
    game.Event = event
    game.Name = name
    game.Description = description
    game.put()
    return game

def DeleteGame(event, name):
    game = GameExist(event, name)
    if not game:
        return False
    e = game[0]
    k = e.put()
    return k.delete()

def DeleteGames(event):
    games = GetGames(event)
    for game in games:
        k = game.put()
        k.delete()
    return games

def UpdateGame(event, name, description):
    print "updating game"
    result = GameExist(event, name)
    if not result:
        return False
    print "updating game"
    game = result[0]
    game.Description = description
    game.put()
    return game

## EventPerson

def CreateEventPerson(username, event, date, location, description):
    result = CreateEvent(event, date, location, description)
    if not result:
        return False
    return AddEventPerson(username, event)

def GetAllEventPerson(username):
    elist = []
    result = EventPerson.query(EventPerson.Username == username).fetch()
    if not result:
        return elist
    for res in result:
        elist.append(res.Event)
    return elists

def GetAllEventByPerson(username):
    elist = GetAllEventByPerson(username)
    result = Event.query(Event.Name.IN(elist)).fetch()
    if not result:
        return False
    return result

def GetEventPerson(username, event):
    result = EventPerson.query(EventPerson.Username == username, EventPerson.Event == event).fetch()
    return result[0]

def AddEventPerson(username, event):
    ep = EventPerson()
    ep.Username = username
    ep.Event = event
    ep.put()
    return result

def DeleteEventPerson(username, event):
    result = GetEventPerson(username, event)
    if not result:
        return False
    k = result.put()
    k.delete()
    return result
