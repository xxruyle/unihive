from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
def home(): 
    return render_template('home.html')

@app.route("/u")
@app.route("/u/<university>")
def university(university=None):
    return render_template('university_home.html', uni=university) 

@app.route("/u/create-university")
def create_university():
    return render_template('create_university.html') 

@app.route("/u")
@app.route("/u/<university>/<course>")
def course(university=None, course=None): 
    return render_template('course.html', uni=university, course=course) 


@app.route("/u")
@app.route("/u/<university>/create-course")
def create_course(university=None): 
    return render_template('create_course.html', uni=university) 

