from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
def home(): 
    return render_template('home.html')

@app.route("/u")
@app.route("/u/<university>")
def university(university=None):
    return render_template('university_home.html', uni=university) 



