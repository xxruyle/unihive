# Filename: main.py
# Description: This module is the entry point of the flask app
# Inputs: Other modules/classes, university, course, session, user, flask
# Output: Entry point of flask app 
# Authors: Xavier Ruyle
# Creation Date: 10/24/2024

import os
import signal
import sys
from functools import wraps

import db
from course import *
from db import connection  # your existing database connection
from db_util import *
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from session import *
from university import *
from user import *
from post import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf'}

DEVELOPMENT = False

app = Flask(__name__) # initialize flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # flask app secret key required for form requests
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



print("*" * 50)
print("Starting UPDATED Flask app - Version 3")
print(f"Python executable: {sys.executable}")
print("*" * 50)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print('\nShutting down gracefully...')
    
    # Close database connection
    if connection:
        print('Closing database connection...')
        connection.close()
    
    # Clear session data
    if SESSION:
        print('Clearing session data...')
        SESSION.current_user_id = None
        USERS.clear()
    
    print('Shutdown complete')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)    # Handles Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)   # Handles termination request

@app.context_processor
def inject_default():
    """Inject default information into HTML templates."""
    return dict(
        USERS   = USERS, 
        SESSION = SESSION,
        active  = None
    )

@app.route("/") 
def home(): 
    '''
    Route function for root page home.html
    Base html Template Dependecies: followed universities, followed courses
    '''
    return render_template('home.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if SESSION.current_user_id is None:
            flash("Please login to access this page")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to home
    if SESSION.current_user_id is not None:
        return redirect(url_for('home'))
        
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Please fill in all fields")
            return redirect(url_for('login'))
            
        # Query the database for the user
        user_data = query(
            "SELECT id, password FROM users WHERE username = ?",
            (username,),
            count=1
        )
        
        if user_data and (DEVELOPMENT or check_password_hash(user_data[1], password)):
            # Set the session user ID
            SESSION.current_user_id = user_data[0]
            USERS[user_data[0]] = User(user_data[0], username) # NOTE: need to store existing user data locally 
            print(SESSION.current_user_id) 
            
            # Update last login timestamp
            query(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user_data[0],)
            )
            
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
            
    return render_template('auth/login.html')

@app.route("/logout")
def logout():
    SESSION.current_user_id = None
    flash("You have been logged out")
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not username or not password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
            
        # Check if username already exists
        existing_user = query(
            "SELECT id FROM users WHERE username = ?",
            (username,),
            count=1
        )
        
        if existing_user:
            USERS[existing_user[0]] = User(existing_user[0], username) # need to insert into local USERS still 
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
            
        # Create new user
        try:
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            
            # Insert new user into database
            query(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?);
                """,
                (username, hashed_password)
            )
            
            # Get the newly created user
            new_user = query(
                "SELECT id, username FROM users WHERE username = ?",
                (username,),
                count=1
            )
            
            if new_user:
                # Update the session with the new user
                SESSION.current_user_id = new_user[0]
                USERS[new_user[0]] = User(new_user[0], username)

                print(SESSION.current_user_id) 
                
                flash('Registration successful! Welcome to UniHive!', 'success')
                return redirect(url_for('home'))
            
        except Exception as e:
            print(f"Registration error: {e}")
            flash('An error occurred during registration.', 'error')
            return render_template('auth/register.html')
    
    # If GET request, just show the registration form
    return render_template('auth/register.html')


@app.route("/profile", methods = ["GET", "POST"])
@login_required
def profile():
    user = USERS.get(SESSION.current_user_id)
    if not user:
        SESSION.current_user_id = None
        return redirect(url_for('login'))


    if request.method == "POST": 
        # upload new profile pic 
        if 'profile_picture' not in request.files: 
            flash("No file selected") 
            return redirect(url_for('profile', user=user, recent_posts=get_posts_user_recent()))
        
        file = request.files['profile_picture']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('profile', user=user, recent_posts=get_posts_user_recent()))

        if file and allowed_file(file.filename): 
            filename = secure_filename("profile_pic.jpg")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('profile', user=user, recent_posts=get_posts_user_recent()))


    return render_template('user_profile.html', user=user, recent_posts=get_posts_user_recent())

@app.route("/u")
@app.route("/u/<university_acro>", methods =["GET", "POST"])
def university(university_acro=None, university_name=None):
    '''
    Route function for university_home.html
    Template Dependecies: University, University courses, followed universities, followed courses
    '''
    current_university = University.get_university_by_acronym(university_acro)

    if current_university is None:
        return render_template('404.html'), 404


    # detect if there is a follow request for the university 
    if request.method == "POST": 
        follow_response = request.form.get('follow-btn') 
        if follow_response: 
            store_university_follow(current_university) # STORE: University follow 

        sort_response = request.form.get('sort-type') 
        if sort_response: 
            print(sort_response) 
            sort_courses(sort_response, current_university)



    # render university home page 
    return render_template('university_home.html', university = current_university)  

@app.route("/create-university", methods =["GET", "POST"])
def create_university():
    '''
    Route function for create_university.html
    Template Dependecies: Followed universities, followed courses
    '''
    # detect POST request 
    if request.method == "POST": 
        # obtain university info to be stored  
        university_name = request.form.get('university')
        university_acro = request.form.get('university-acro')
        # correct data check
        if university_name and university_acro and University.get_university_by_acronym(university_acro) is None: 
            store_university(university_name, university_acro) # STORE: University 
            return redirect(url_for('university') + '/' + university_acro) # redirect to university home page  
        else: 
            flash("University already exists", 'error') # Inform user that university already exists
    # render create university page
    return render_template('create_university.html')  

@app.route("/u")
@app.route("/u/<university_acro>/<course>", methods=['GET', 'POST'])
def course(university_acro=None, course=None): 
    '''
    Route function for course.html
    Template Dependecies: University acro, Course, followed universities, followed courses
    '''
    stored_university, stored_course = get_uni_and_course_from_route(university_acro, course)

    if stored_university is None or stored_course is None:
        return render_template('404.html'), 404

    # detect if there was a post request 
    if request.method == "POST": 
        # handle post creation 
        post_title = request.form.get('post-title')
        post_body = request.form.get('post-body')
        if post_title and post_body: # data check 
            # store the post 
            store_post(stored_course, post_title, post_body) # STORE: user post  
            # redirect so it doesn't resend the post request 
            return redirect(url_for('course', university_acro=stored_university.acronym, course=stored_course.name_combined))



        # handle follow request 
        follow_response = request.form.get('follow-btn') 
        if follow_response: 
            store_course_follow(stored_course) # STORE: course follow

        # handle course info submission
        grade        = request.form.get('grade')
        difficulty   = request.form.get('difficulty')
        credit_hours = request.form.get('credit-hours')

        # data check
        if grade and difficulty and credit_hours: 
            # Store course grade, difficulty, and hours info
            store_course_info(
                stored_course, 
                int(difficulty), 
                Grade.letter_to_grade(grade), 
                int(credit_hours)
            )

        # handle professor info submission
        professor_first_name = request.form.get('first-name')
        professor_last_name  = request.form.get('last-name')

        # correct data check
        if professor_first_name and professor_last_name: 
            store_professor_info(stored_course, f"{professor_first_name} {professor_last_name}") # STORE: Professor info


        # handle syllabus submission
        if 'syllabusFile' in request.files: # make sure the submission exists
            file = request.files['syllabusFile'] # get the file data
            # TODO: Make sure the file is a supported file type (pdf, docx)
            if file == '': # the file was not found
                flash("File not found") 


            if allowed_file(file.filename): 
                filename = secure_filename(file.filename)  
                # store the syllabus file into database
                store_syllabus(stored_course.name_combined, filename, file.read()) 
                # DEBUG (to make sure it was inserted into the db): 
                print(query("SELECT coursename FROM syllabus;"))
                return redirect(url_for('course', university_acro=stored_university.acronym, course=stored_course.name_combined))
            else: 
                flash("That file type is not allowed")
                return redirect(url_for('course', university_acro=stored_university.acronym, course=stored_course.name_combined))

        # handle syllabus download 

        # handle sort posts request 
        sort_response = request.form.get('sort-type')
        if sort_response: 
            sort_posts(sort_response, stored_course) 

    return render_template('course.html', course = stored_course)  # render course html 


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
        department      = request.form.get('department').lower()
        course_number   = request.form.get('course-number').lower()

        # Get the university using the supplied acronym
        stored_university = University.get_university_by_acronym(university_acro)

        # If the university doesn't exist, error out
        if stored_university is None:
            flash("University does not exist")
            return render_template('create_course.html', uni=university)

        # Get the requested department from the DB
        stored_department = Department.get_department_by_abbreviation(stored_university, department)

        # Just in case the department doesn't already exist
        if stored_department is None:
            # Create a new department and use it
            store_department(department, department, stored_university)
            stored_department = Department.get_department_by_abbreviation(stored_university, department)

        # Get the requested course from the DB
        stored_course = Course.get_course_by_course_number(stored_university, stored_department, course_number)

        # check if course exists
        if stored_course is None: 
            # TODO: course name should be a form option 
            store_course("", course_number, stored_department) # STORE: Course obj
            stored_course = Course.get_course_by_course_number(stored_university, stored_department, course_number)

            return redirect(url_for('course', university_acro=stored_university.acronym, course=stored_course.name_combined)) # redirect user to the course page 
        else: 
            flash("Course already exists", 'error') # Inform user that course exists

    return render_template('create_course.html', uni=university)  # render create course page 

@app.route("/user/<username>", methods=["GET", "POST"])
def profile_page(username):
    user = User.get_user_by_username(username) 

    if user is None:
        return render_template("404.html"), 404
    
    return render_template("user_profile.html", user = user, active = "profile-page", recent_posts=get_posts_user_recent())

@app.route("/download/<coursename>/<filename>") 
def download(filename, coursename): 
    """
    Shows the user the chosen file in the browser 
    User can download or preview the file
    """
    return download_syllabus(filename, coursename) 

@app.route("/u/<university_acro>/<course_name>/<post_identifier>", methods=['GET', 'POST'])
def post(university_acro=None, course_name=None, post_identifier=None):

    # Get the university and course of the post. Its okay if
    # these become None since the post getter does not care.
    university = University.get_university_by_acronym(university_acro)
    course     = Course.get_course_by_name_combined(university, course_name)

    # Get the post object by title.
    post = Post.get_post_by_title(post_identifier, course)

    # Couldn't get post by title, try ID instead.
    if post is None:
        post = Post.get_post_by_id(post_identifier)

    # 404 if the post wasn't found.
    if post is None:
        return render_template("404.html"), 404
    
    if request.method == "POST":
        user = User.get_user_by_id(SESSION.current_user_id)
       
        if user is not None:
            if request.form.get("like-btn"):
                post.toggle_like(user)
            
            if request.form.get("dislike-btn"):
                post.toggle_dislike(user)

            if request.form.get("reply-parent"):
                replied_post = Post.get_post_by_id(int(request.form.get("reply-parent")))
                replied_post.add_reply(user, request.form.get("reply-body"))
        
        flash("Must be logged in to preform this action.")
        return render_template("login.html")


    # Return the post HTML template.
    return render_template("post.html", post=post)

def main(): 
    '''
    Entry point for app
    '''
    try:
        app.run(debug=True, host='localhost', port=5001)
        print("It's running here")
    except KeyboardInterrupt:
        # This will trigger our signal handler
        pass

if __name__ == "__main__": 
    print("RUNNING")
    main()

