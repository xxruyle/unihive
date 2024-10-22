from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/") 
def home(): 
    return render_template('home.html')

@app.route("/u")
@app.route("/u/<university>")
def university(university=None):
    return render_template('university_home.html', uni=university) 

@app.route("/create-university", methods =["GET", "POST"])
def create_university():
    if request.method == "POST": 
        university = request.form.get('university')
        university_acro = request.form.get('university-acro')
        return redirect(url_for('university', university=university_acro))

    return render_template('create_university.html') 

@app.route("/u")
@app.route("/u/<university>/<course>")
def course(university=None, course=None): 
    return render_template('course.html', uni=university, course=course) 


@app.route("/create-course", methods=["GET", "POST"])
def create_course(university="placeholder"): 
    if request.method == "POST": 
        university = request.form.get('university')
        department = request.form.get('department')
        course_number = request.form.get('course-number')
        return redirect(url_for('course', university=university, course=f"{department}-{course_number}"))


    return render_template('create_course.html', uni=university) 

