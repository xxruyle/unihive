from flask import Flask, render_template, request, redirect, url_for, flash
from university import *
from course import * 

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/") 
def home(): 
    return render_template('home.html', UNIVERSITIES=UNIVERSITIES)

@app.route("/u")
@app.route("/u/<university_acro>")
def university(university_acro=None, university_name=None):
    return render_template('university_home.html', university_acro=university_acro, university_name=university_name, courses=UNIVERSITIES[university_acro].courses, UNIVERSITIES=UNIVERSITIES) 

@app.route("/create-university", methods =["GET", "POST"])
def create_university():
    if request.method == "POST": 
        university_name = request.form.get('university').lower()
        university_acro = request.form.get('university-acro').lower()
        if university_name and university_acro and (university_name not in UNIVERSITIES): 
            university = University(len(UNIVERSITIES) + 1, university_name, university_acro)
            UNIVERSITIES[university_acro] = university
            print(UNIVERSITIES) 
            return redirect(url_for('university', university_acro=university_acro))
        else: 
            flash("University already exists", 'error') # TODO: implement this message in the front endj
        

    return render_template('create_university.html', UNIVERSITIES=UNIVERSITIES) 

@app.route("/u")
@app.route("/u/<university_acro>/<course>", methods=['GET', 'POST'])
def course(university_acro=None, course=None): 
    if request.method == "POST": 
        print(request.form)
        grade = request.form.get('grade').upper()
        difficulty = int(request.form.get('difficulty'))
        credit_hours = int(request.form.get('credit-hours'))

        print(type(difficulty))
        courseObj = UNIVERSITIES[university_acro].courses[course].store_info(grade, difficulty, credit_hours)

 
    return render_template('course.html', uni=university_acro, course=course, UNIVERSITIES=UNIVERSITIES) 


@app.route("/create-course", methods=["GET", "POST"])
def create_course(university="placeholder"): 
    if request.method == "POST": 
        university_acro = request.form.get('university').lower()
        department = request.form.get('department').lower()
        course_number = request.form.get('course-number').lower()

        if university_acro in UNIVERSITIES: 
            department_course_number = f"{department}-{course_number}"
            if department_course_number not in UNIVERSITIES[university_acro].courses: 
                # TODO: course id is 0 for now 
                # TODO: course name should be a form option 
                course_obj = Course(len(UNIVERSITIES[university_acro].courses) + 1, course_number, department, "")
                UNIVERSITIES[university_acro].courses[department_course_number] = course_obj
                return redirect(url_for('course', university_acro=university_acro, course=department_course_number))
            else: 
                flash("Course already exists", 'error') # TODO: implement this message in the front endj
        else: 
            flash("University does not exist", 'error') # TODO: implement this message in the front endj

    return render_template('create_course.html', uni=university, UNIVERSITIES=UNIVERSITIES) 

