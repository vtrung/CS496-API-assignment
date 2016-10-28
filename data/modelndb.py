# [START imports]
from flask import Flask, render_template, request, redirect, url_for
# [END imports]

from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    birthdate = ndb.StringProperty()
    gender = ndb.StringProperty()
    skill = ndb.IntegerProperty()
    teacher = ndb.BooleanProperty()
    ta = ndb.BooleanProperty()
    student = ndb.BooleanProperty()

class Event(ndb.Model):
    Name = ndb.StringProperty()
    Date = ndb.StringProperty()
    Description = ndb.StringProperty()
    Location = ndb.StringProperty()

class Game(ndb.Model):
    Event = ndb.StringProperty()
    Name = ndb.StringProperty()
    Description = ndb.StringProperty()

class Person(ndb.Model):
    Username = ndb.StringProperty()
    Name = ndb.StringProperty()
    Gender = ndb.StringProperty()
    Age = ndb.IntegerProperty()
