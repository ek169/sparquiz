#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import jinja2
from models import User, Set, Question, Class, School
from google.appengine.ext import db
from google.appengine.api import memcache
import re
import os
import hashutils
from random import shuffle
from populate_schools import pop_schools
import json

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

pop_schools()

class MainHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

class UserHandler(MainHandler):

    def getCookieCacheUser(self):
        user_id = self.read_secure_cookie('user_id')
        if user_id:
            user = memcache.get(user_id)
            if type(user) is User:
                return user
            else:
                user = User.get_by_id(int(user_id))
                if user:
                    memcache.set(user_id, user)
                    return user

    def cacheClass(self, user_key, class_name):
        class_obj = memcache.get(str(user_key)+class_name)
        if type(class_obj) is Class:
            return class_obj
        else:
            class_obj = Class.all().filter('name =', class_name).filter('other_users ==', str(user_key)).get()
            memcache.set(str(user_key)+class_name, class_obj)
            return class_obj


    def cacheClassSets(self, class_obj):
        class_sets = memcache.get(str(class_obj.key().id()))
        if type(class_sets) is list:
            return class_sets
        else:
            class_sets = Set.all().filter('class_name =', class_obj)
            memcache.set(str(class_obj.key().id()), class_sets)
            return class_sets

    def cacheAllUserClasses(self, user_key):
        all_user_classes = memcache.get(str(user_key)+"all")
        if type(all_user_classes) is list:
            return all_user_classes
        else:
            all_user_classes = Class.all().filter('other_users ==', str(user_key)).order("last_updated")
            memcache.set(str(user_key)+"all", all_user_classes)
            return all_user_classes


    def cacheSet(self, set_name, class_obj):
        set_obj = memcache.get(str(class_obj.key().id())+set_name)
        if type(set_obj) is Set:
            return set_obj
        else:
            set_obj = Set.all().filter("class_name =", class_obj).filter("name =", set_name).get()
            memcache.set(str(class_obj.key().id()) + set_name, set_obj)
            return set_obj

    def cacheQuestions(self, class_obj, set_obj):
        questions = memcache.get(str(class_obj.key().id()) + str(set_obj.name) + 'q')
        if type(questions) is list:
            return questions
        else:
            questions = self.get_questions_by_set(set_obj)
            memcache.set(str(class_obj.key().id()) + str(set_obj.name) + 'q', questions)
            return questions

    def get_user_by_name(self, user_input):
        user = User.all().filter('username =', user_input)
        if user:
            return user.get()

    def get_set_by_user(self, user, set_name):
        set_name = Set.all().filter('user =', user).filter('name =', set_name)
        if set_name:
            return set_name.get()

    def get_questions_by_set(self, set_obj):
        questions = Question.all().filter('set_name =', set_obj).order('last_edited')
        return questions

    def get_question_by_id(self, question_id):
        question = Question.get_by_id(int(question_id))
        if question:
            return question


    def login_user(self, user):
        user_id = user.key().id()
        self.set_secure_cookie('user_id', str(user_id))

    def logout_user(self):
        self.set_secure_cookie('user_id', '')

    def set_secure_cookie(self, name, user_id):
        cookie_val = hashutils.make_secure_cookie(user_id)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return hashutils.validate_cookie(cookie_val)

    def get_post_by_name(self, title):
        post = db.GqlQuery("select * from Post where title = '%s and '" % title)
        if post:
            post.get()


class Index(UserHandler):

    def get(self):
        user = self.getCookieCacheUser()
        if user:
            the_classes = Class.all().filter("user_creator !=", user)
            user_classes = self.cacheAllUserClasses(user.key().id())
            page_title = "Welcome " + user.username
            self.render('index.html', current_user=user, the_classes=the_classes,
                        page_title=page_title, user_classes=user_classes)
        else:
            the_classes = Class.all()
            page_title = "Welcome To Sparquiz"
            self.render('index.html', current_user=None, the_classes=the_classes, page_title=page_title)


class createClass(UserHandler):
    def get(self, username=""):
        user = self.getCookieCacheUser()
        if username == user.username:
            schools = School.all()
            self.render("create-class.html", current_user=user, schools=schools, page_title="Create New Class", class_active="active")

    def post(self, username=""):
        user = self.getCookieCacheUser()
        class_name = self.request.get("class-name")
        class_instructor = self.request.get("class-instructor")
        class_year = self.request.get("year")
        school_id = self.request.get("school_id")
        school = School.get_by_id(int(school_id))
        if class_name and class_instructor and class_year and school:
            new_class = Class(name=class_name, school=school, instructor=class_instructor, year=int(class_year),
                              user_creator=user, requests=[])
            new_class.other_users.append(str(user.key().id()))
            new_class.put()
            memcache.set(str(user.key().id()) + class_name, new_class)
            memcache.delete(str(user.key().id()))
            self.redirect("/%s/%s" % (user.username, new_class.name))
        else:
            schools = School.all()
            self.render("create-class.html", schools=schools, class_name=class_name, class_instructor=class_instructor, year=class_year, class_active="active")

class viewClass(UserHandler):
    def get(self, username="", class_name=""):
        user = self.getCookieCacheUser()
        if type(user) == User:
            if user.username == username:
                class_obj = self.cacheClass(user.key().id(), class_name)
                the_class_sets = self.cacheClassSets(class_obj)
                user_requests = []
                if len(class_obj.requests) > 0:
                    for user_id in class_obj.requests:
                        user_who_requests = User.get_by_id(int(user_id))
                        if type(user_who_requests) is User:
                            user_requests.append(user_who_requests)
                self.render("editclassview.html", current_user=user, class_obj=class_obj,
                            the_class_sets=the_class_sets, current_id=str(user.key().id()), user_requests=user_requests,
                            class_active="active",
                            page_title=str(class_obj.name) + ' (' + str(class_obj.year) + ')')
            else:
                user_creator = self.get_user_by_name(username)
                try:
                    class_obj = self.cacheClass(user_creator.key().id(), class_name)
                    the_class_sets = self.cacheClassSets(class_obj)
                    have_requested = None
                    if unicode(user.key().id()) in class_obj.other_users:
                        self.redirect("/%s/%s" % (user.username, class_name))
                    elif unicode(user.key().id()) in class_obj.requests[:]:
                        have_requested = True
                    else:
                        have_requested = False
                    self.render("classview.html", have_requested=have_requested, current_user=user, user_creator=user_creator,
                            class_obj=class_obj, the_class_sets=the_class_sets, page_title=str(class_obj.name))
                except AttributeError:
                    self.write("There is either no user or class by that name")
        else:
            self.render("login.html", error="You must be logged in to view this class")



class addClass(UserHandler):
    def get(self, username="", class_name=""):
        user = self.getCookieCacheUser()
        user_creator = self.get_user_by_name(username)
        class_obj = Class.all().filter('name =', class_name).filter('user_creator =', user_creator).get()
        if user and user_creator and class_obj:
            if str(user.key().id()) not in class_obj.requests and str(user.key().id()) not in class_obj.other_users:
                class_obj.requests.append(str(user.key().id()))
                class_obj.put()
                memcache.delete(str(user_creator.key().id())+class_name)
                my_response = {'msg': 'Request Sent!'}
                json_response = json.dumps(my_response)
                self.response.headers.add_header('content-type', 'text/json', charset='utf-8')
                self.response.out.write(json_response)
        else:
            self.write("We cannot process your request")

    def post(self, username="", class_name=""):
        data = json.loads(self.request.body)
        answer = data['answer']
        uid = data['uid']
        print(answer, uid)
        user = self.getCookieCacheUser()
        if user.username == username:
            class_obj = self.cacheClass(user.key().id(), class_name)
            if answer == "Allow":
                class_obj.other_users.append(uid)
                class_obj.requests.remove(str(uid))
                class_obj.put()
            elif answer == "Deny":
                class_obj.requests.remove(uid)
                class_obj.put()
            memcache.delete(str(user.key().id())+class_name)
            my_response = {'msg': 'success'}
            json_response = json.dumps(my_response)
            self.response.headers.add_header('content-type', 'text/json', charset='utf-8')
            self.response.out.write(json_response)








class createSet(UserHandler):
    def get(self, username="", class_name=""):
        user = self.getCookieCacheUser()
        class_obj = self.cacheClass(user.key().id(), class_name)
        if username == user.username:
            self.render("createset.html", current_user=user, class_obj=class_obj,
                        class_name=class_name, class_active="active",
                        current_id=str(user.key().id()), page_title=str(class_obj.name)+" - New Set")
        else:
            self.render("login.html")

    def post(self, class_name="", username=""):
        set_name = self.request.get('set-title')
        set_description = self.request.get('set-description')
        user = self.getCookieCacheUser()
        if set_name and set_description and class_name:
            if user:
                class_obj = memcache.get(str(user.key().id()) + class_name)
                if type(class_obj) is not Class:
                    class_obj = self.cacheClass(user.key().id(), class_name)
                new_set = Set(name=set_name, description=set_description, total_attempts=0, total_scores=0,
                              user=user, class_name=class_obj)
                new_set.put()
                memcache.set(str(class_obj.key().id())+set_name, new_set)
                self.redirect("/%s/%s/%s" % (username, class_name, set_name))
        else:
            self.render("createset.html", current_user=user, set_name=set_name,
                        set_description=set_description, class_name=class_name, current_id=str(user.key().id()),
                        class_active="active", page_title=class_name)


class viewSet(UserHandler):
    def get(self, set_name="", class_name="", username=""):
        user = self.getCookieCacheUser()
        if user:
            if username == user.username:
                class_obj = self.cacheClass(user.key().id(), class_name)
                set_obj = self.cacheSet(set_name, class_obj)
                questions = self.cacheQuestions(class_obj, set_obj)
                if set_obj:
                    self.render("setview.html", questions=questions, current_id=str(user.key().id()),
                            class_obj=class_obj, set_obj=set_obj,
                            current_user=user, class_active="active", page_title=set_name)
                else:
                    self.write("You do not have permission to view this set")
            else:
                self.redirect("/")
        else:
            self.render("login.html", error="You do not have permission to view this set")


class createQuestion(UserHandler):

    question_types = ['check', 'multiple', 'true/false']

    def get(self, set_name="", username="", class_name=""):
        user = self.getCookieCacheUser()
        if username == user.username:
            class_obj = memcache.get(str(user.key().id())+class_name)
            if type(class_obj) is not Class:
                class_obj = self.cacheClass(user.key().id(), class_name)
            set_obj = memcache.get(str(class_obj.key().id())+set_name)
            if type(set_obj) is not Set:
                set_obj = self.cacheSet(set_name, class_obj)
            if type(set_obj) is Set:
                self.render("create-question.html", set_obj=set_obj, class_obj=class_obj, current_user=user, current_id=str(user.key().id()),
                class_active="active", page_title="New Question")
            else:
                self.redirect("/")

    def post(self, set_name="", username="", class_name=""):
        user = self.getCookieCacheUser()
        if user.username == username:
            question_type = self.request.get("questionType")
            question = self.request.get("question")
            class_obj = self.cacheClass(user.key().id(), class_name)
            set_obj = self.cacheSet(set_name, class_obj)
            if question_type == 'check':
                correct_answer = []
                for i in range(1, 5):
                    correct_ans = self.request.get('correctAnswer' + str(i))
                    if correct_ans:
                        correct_answer.append(correct_ans)
                    else:
                        break
            else:
                correct_answer = self.request.get("correctAnswer1")

            other_answers = []
            for i in range(1, 5):
                other_ans = self.request.get('otherAnswers' + str(i))
                if other_ans:
                    other_answers.append(other_ans)
                else:
                    break

            if question_type == "true/false":
                if correct_answer == 'true':
                    other_answers = ['false']
                elif correct_answer == 'false':
                    other_answers = ['true']

            other_answers_is_true = False
            if len(other_answers) > 0:
                other_answers_is_true = True
            if question and correct_answer and question_type and other_answers_is_true:
                if type(correct_answer) == list:
                    for a in correct_answer:
                        other_answers.append(a)
                else:
                    other_answers.append(correct_answer)

                shuffle(other_answers)
                q = Question(set_name=set_obj, question=question,
                             type=question_type, other_answers=other_answers,
                             multiple_correct_answers=[], total_attempts=0, correct_attempts=0)
                if question_type == 'check':
                    q.multiple_correct_answers = correct_answer
                else:
                    q.correct_answer = correct_answer
                q.put()
                set_obj.put()
                memcache.delete(str(class_obj.key().id())+ str(set_obj.name) + 'q')
                self.redirect("/%s/%s/%s" % (user.username, class_obj.name, set_obj.name))
            else:
                self.render("create-question.html", type=question_type, current_user=user, set_obj=set_obj,
                        class_obj=class_obj, question=question, current_id=str(user.key().id()),
                            correct_answer=correct_answer, class_active="active")
        else:
            self.redirect("/")

class editQuestion(UserHandler):
    def get(self, set_name="", question_id="", username="", class_name=""):
        user = self.getCookieCacheUser()
        if user.username == username:
            class_obj = self.cacheClass(user.key().id(), class_name)
            question = self.get_question_by_id(question_id)
            set_obj = self.cacheSet(set_name, class_obj)
            if question.set_name.key().id() == set_obj.key().id():
                self.render("editquestion.html", question=question, current_id=str(user.key().id()),
                            set_name=set_name, current_user=user, class_active="active", page_title="Edit Question")
            else:
                self.write("Error 404")
        else:
            self.write("Error 404")

    def post(self, set_name="", question_id="", username="", class_name=""):
        q = self.get_question_by_id(question_id)
        user = self.getCookieCacheUser()
        question_text = self.request.get("question")
        correct_answer = self.request.get("correctAnswer")
        other_answers = self.request.get_all("otherAnswers")
        if question_text and correct_answer and other_answers:
            class_obj = self.cacheClass(user.key().id(), class_name)
            set_obj = self.cacheSet(set_name, class_obj)
            other_answers.append(correct_answer)
            shuffle(other_answers)
            q.set_name = set_obj
            q.question = question_text
            q.correct_answer = correct_answer
            q.other_answers = other_answers
            q.put()
            set_obj.put()
            memcache.delete(str(user.key().id())+set_name)
            self.redirect("/%s/%s/%s" % (username, class_name, set_name))
        else:
            self.render("editquestion.html", question=q, set_name=set_name)


class practiceSet(UserHandler):


    def get(self, set_name="", username="", class_name=""):
        user = self.getCookieCacheUser()
        class_obj = self.cacheClass(user.key().id(), class_name)
        set_obj = self.cacheSet(set_name, class_obj)
        questions = self.cacheQuestions(class_obj, set_obj)
        if set_obj:
            page_title = "Practice: " + str(set_obj.name)
            self.render("practicequiz.html", questions=questions, current_id=str(user.key().id()),
                        current_user=user, class_obj=class_obj, set_obj=set_obj, class_active="active", page_title=page_title)

    def post(self, username="", set_name="", class_name=""):
        user = self.getCookieCacheUser()
        class_obj = self.cacheClass(user.key().id(), class_name)
        set_obj = self.cacheSet(set_name, class_obj)
        questions = self.cacheQuestions(class_obj, set_obj)
        total_correct = 0.0
        total_answered = 0.0
        question_results = []
        for question in questions:
            if question.type == 'check':
                answer = self.request.get_all(str(question.key().id()))
            else:
                answer = self.request.get(str(question.key().id()))

            if answer:
                total_answered += 1
                if answer == question.correct_answer or all(a in question.multiple_correct_answers for a in answer):
                    total_correct += 1
                    correct = int(question.correct_attempts) + 1
                    total = int(question.total_attempts) + 1
                    question.correct_attempts = correct
                    question.total_attempts = total
                    question.difficulty = int(question.correct_attempts)/int(question.total_attempts)*100.0
                    shuffle(question.other_answers)
                    question.put()
                    question_results.append([True, question, answer])
                else:
                    total = question.total_attempts+1
                    question.total_attempts = total
                    shuffle(question.other_answers)
                    question.put()
                    question_results.append([False, question, answer])

        if total_answered > 0:
            attempt_score = round(((total_correct/total_answered)*100), 2)
            sum_score = int(set_obj.total_scores+attempt_score)
            total_attempts = set_obj.total_attempts+1
            set_obj.total_scores = sum_score
            set_obj.total_attempts = total_attempts
            set_obj.put()
            self.render("practice-results.html", current_user=user, class_active="active", current_id=str(user.key().id()),
                        question_results=question_results, class_obj=class_obj, set_obj=set_obj, attempt_score=attempt_score, page_title="Practice Results")


class practiceQuestion(UserHandler):
    def get(self, set_name="", question_id="", username="", class_name=""):
        user = self.getCookieCacheUser()
        question = self.get_question_by_id(question_id)
        self.render("practicequestion.html", question=question, current_user=user, class_active="active")

    def post(self, set_name="", question_id="", username="", class_name=""):
        question = self.get_question_by_id(question_id)
        if question.type == 'check-box':
            answer = self.request.get_all(str(question_id))
        else:
            answer = self.request.get(str(question_id))

        if answer == question.correct_answer or all(a in question.multiple_correct_answers for a in answer):
            self.write("You are correct")
        else:
            self.write("You are incorrect")


class Login(UserHandler):
    def get(self):
        self.render('login.html', login_active="active", page_title="Login")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user_obj = self.get_user_by_name(username)

        if user_obj is None:
            self.render('login.html', user_error="Invalid Username",  page_title="Login")
        elif hashutils.validate_pw(username, password, user_obj.pw_hash):
            self.login_user(user_obj)
            self.redirect('/')
        else:
            self.render('login.html', page_title="Login", password_error="Incorrect Password", username=username)

class Logout(UserHandler):

    def get(self):
        self.logout_user()
        self.redirect('/login')

class Signup(UserHandler):
    def get(self):
        self.render('signup.html', sign_up_active="active", page_title="Sign Up")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = {}
        has_error = False

        if not self.validate_username(username):
            has_error = True
        elif self.get_user_by_name(username):
            params['user_error'] = "That username already exists"
            has_error = True

        if not self.validate_pw(password):
            has_error = True
        elif password != verify:
            params['pw_error'] = "Your passwords do not match"
            has_error = True

        if not self.validate_email(email):
            has_error = True

        if has_error:
            self.render('signup.html', sign_up_active="active", page_title="Sign Up", **params)
        else:
            pw_hash = hashutils.make_pw_hash(username, password)
            u = User(username=username, pw_hash=pw_hash, email=email, sets=[])
            u.put()
            self.login_user(u)
            self.redirect('/')

    def validate_pw(self, password):
        pw_requirements = re.compile(r"^(?=(.*\d){0})(?=.*[a-z]).{4,}$")
        if pw_requirements.match(password):
            return password
        else:
            return ""

    def validate_username(self, username):
        un_requirements = re.compile(r"^.{5,}$")
        if un_requirements.match(username):
            return username
        else:
            return ""

    def validate_email(self, email):
        email_requirements = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email_requirements.match(email):
            return email
        else:
            return ""

class ViewProfile(UserHandler):
    def get(self, username=""):
        user = self.getCookieCacheUser()
        if user:
            if user.username == username:
                classes = Class.all().filter("other_users ==", str(user.key().id())).order("last_updated")
                page_title = "List of Classes"
                self.render('edituserprofile.html', page_title=page_title, current_user=user, classes=classes, class_active="active")
        else:
            user_profile = self.get_user_by_name(username)
            self.render('userprofile.html', user_profile=user_profile)



    def post(self, username=''):
        current_user = self.get_user_by_name(username)
        age = self.request.get('age')

        params = {}
        has_error = False


        if not self.validate_age(age):
            params['age_error'] = "That is not a valid age"
            has_error = True


        if has_error:
            params['current_user'] = current_user
            self.render('edituserprofile.html', **params)
        else:
            current_user.age = int(age)
            current_user.put()
            self.render('edituserprofile.html', current_user=current_user)


    def validate_age(self, age):
        try:
            age = int(age)
            if int and 10 < age < 99:
                return age
            else:
                return ""
        except ValueError:
            return ""









app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/add', addClass),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/create-class', createClass),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>', viewClass),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/create-set', createSet),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>', viewSet),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>', ViewProfile),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/new-question/', createQuestion),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/<question_id>', editQuestion),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/practice/', practiceSet),
    webapp2.Route('/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/practice/<question_id>', practiceQuestion),


], debug=True)

auth_paths = [
    '/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/new-question/',
    '/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/create-set/',
    '/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/<practice>',
    '/<username:[a-zA-Z0-9_-]{3,20}>/<class_name>/<set_name>/practice/<question_id>',
]
