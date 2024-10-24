# Filename: main.py
# Description: This module is the entry point of the flask app
# Inputs: Other modules/classes, university, course, session, user, flask
# Output: Entry point of flask app 
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

from flask import Flask, render_template, request, redirect, url_for, flash
from university import *
from course import * 
from session import * 
from user import * 
from db_util import * 
import db

app = Flask(__name__) # initialize flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # flask app secret key required for form requests

@app.route("/") 
def home(): 
    '''
    Route function for root page home.html
    Base html Template Dependecies: followed universities, followed courses
    '''
    return render_template('home.html', UNIVERSITIES=UNIVERSITIES, USERS=USERS, SESSION=SESSION)

@app.route("/u")
@app.route("/u/<university_acro>", methods =["GET", "POST"])
def university(university_acro=None, university_name=None):
    '''
    Route function for university_home.html
    Template Dependecies: University, University courses, followed universities, followed courses
    '''
    # detect if there is a follow request for the university 
    if request.method == "POST": 
        follow_response = request.form.get('follow-btn') 
        if follow_response: 
            store_university_follow(university_acro) # STORE: University follow 


    # render university home page 
    return render_template('university_home.html', university_acro=university_acro.lower(), university_name=university_name, courses=UNIVERSITIES[university_acro.lower()].courses, UNIVERSITIES=UNIVERSITIES, USERS=USERS, SESSION=SESSION)  

@app.route("/create-university", methods =["GET", "POST"])
def create_university():
    '''
    Route function for create_university.html
    Template Dependecies: Followed universities, followed courses
    '''
    # detect POST request 
    if request.method == "POST": 
        # obtain university info to be stored  
        university_name = request.form.get('university').lower()
        university_acro = request.form.get('university-acro').lower()
        # correct data check
        if university_name and university_acro and not (university_exists(university_acro)): 
            store_university(university_acro, university_name) # STORE: University 
            return redirect(url_for('university', university_acro=university_acro)) # redirect to university home page  
        else: 
            flash("University already exists", 'error') # Inform user that university already exists
    # render create university page
    return render_template('create_university.html', UNIVERSITIES=UNIVERSITIES, USERS=USERS, SESSION=SESSION)  

@app.route("/u")
@app.route("/u/<university_acro>/<course>", methods=['GET', 'POST'])
def course(university_acro=None, course=None): 
    '''
    Route function for course.html
    Template Dependecies: University acro, Course, followed universities, followed courses
    '''
    # detect if there was a post request 
    if request.method == "POST": 
        # handle follow request 
        follow_response = request.form.get('follow-btn') 
        if follow_response: 
            store_course_follow(university_acro, course) # STORE: course follow

        # handle course info submission
        grade = request.form.get('grade')
        difficulty = request.form.get('difficulty')
        credit_hours = request.form.get('credit-hours')

        # data check
        if grade and difficulty and credit_hours: 
            store_course_info(UNIVERSITIES[university_acro].courses[course], grade.upper(), int(difficulty), int(credit_hours)) # STORE: Course info

        # handle professor info submission
        professor_first_name = request.form.get('first-name')
        professor_last_name = request.form.get('last-name')
        # correct data check
        if professor_first_name and professor_last_name: 
            store_professor_info(UNIVERSITIES[university_acro].courses[course], f"{professor_first_name} {professor_last_name}") # STORE: Professor info

    return render_template('course.html', uni=university_acro, course=course, UNIVERSITIES=UNIVERSITIES, USERS=USERS, SESSION=SESSION)  # render course html 


@app.route("/create-course", methods=["GET", "POST"])
def create_course(university="placeholder"): 
    '''
    Route function for create course page 
    Template Dependecies: followed universities, followed courses
    '''
    # detect post request 
    if request.method == "POST": 
        # handle create course info
        university_acro = request.form.get('university').lower()
        department = request.form.get('department').lower()
        course_number = int(request.form.get('course-number').lower())

        # check if university exists  
        if university_acro in UNIVERSITIES: 
            department_course_number = f"{department}-{course_number}"
            if not course_exists(university_acro, f"{department}-{course_number}"): 
                # TODO: course name should be a form option 
                store_course(len(UNIVERSITIES[university_acro].courses) + 1, course_number, department, "", university_acro) # STORE: Course obj

                return redirect(url_for('course', university_acro=university_acro, course=department_course_number)) # redirect user to the course page 
            else: 
                flash("Course already exists", 'error') # Inform user that course exists
        else: 
            flash("University does not exist", 'error') # Inform user that university doesn't exists

    return render_template('create_course.html', uni=university, UNIVERSITIES=UNIVERSITIES, USERS=USERS, SESSION=SESSION)  # render create course page 

def main(): 
    '''
    Entry point for app
    '''
    # DEBUG: university of kansas is added as the first university 
    UNIVERSITIES["ku"] = University(1, "university of kansas", "ku") # STORE: University
    UNIVERSITIES["ku"].courses["eecs-581"] = Course(1, 581, "eecs", "", "ku") # adding eecs 581 as a course

    # DEBUG: first person is added to the session
    daemon_user = User(1, "Jonathon Blow")
    daemon_user.followed_universities.add(UNIVERSITIES["ku"])
    USERS[1] = daemon_user # STORE: user 

    # run the flask web server 
    app.run(debug=True)

if __name__ == "__main__": 
    main()

