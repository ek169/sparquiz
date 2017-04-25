from google.appengine.ext import db


class School(db.Model):
    name = db.StringProperty(required=True)
    state = db.StringProperty(required=True)
    classes = db.ListProperty(int)


class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=True)


class Class(db.Model):
    name = db.StringProperty(required=True)
    instructor = db.StringProperty(required=True)
    year = db.IntegerProperty(required=True)
    last_updated = db.DateTimeProperty(auto_now_add=True)
    school = db.ReferenceProperty(School)
    user_creator = db.ReferenceProperty(User)
    other_users = db.StringListProperty()
    requests = db.StringListProperty()


class Set(db.Model):
    name = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    last_updated = db.DateProperty(auto_now_add=True)
    total_attempts = db.IntegerProperty(required=False)
    total_scores = db.IntegerProperty(required=False)
    user = db.ReferenceProperty(User)
    class_name = db.ReferenceProperty(Class)


class Question(db.Model):
    question = db.StringProperty(required=True)
    correct_answer = db.StringProperty(required=False)
    multiple_correct_answers = db.StringListProperty(required=True)
    other_answers = db.StringListProperty(required=True)
    last_edited = db.DateTimeProperty(auto_now_add=True)
    type = db.StringProperty(required=True)
    total_attempts = db.IntegerProperty(required=True)
    correct_attempts = db.IntegerProperty(required=True)
    difficulty = db.FloatProperty(required=False)
    set_name = db.ReferenceProperty(Set)




