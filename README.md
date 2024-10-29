# UniHive 
UniHive is what is happening on your campus academically.   

Serving the academic discourse. 

A project made for EECS 581 (Software Engineering II) 
![](app/static/unihive_course_page.png)

## Setup 
1) Make a virtual environment
```
$ python -m venv .venv
```
2) activate the virtual environment 

```
. .venv/bin/activate
```

3) install flask
```
$ pip install Flask
```

Or follow the official Flask docs: https://flask.palletsprojects.com/en/3.0.x/installation/

## Usage 
In the project root directory: 
```
$ python3 app/main.py
```

## Tech Stack 
- Flask 
- Postgre SQL
- Bootstrap 


## Tips
When working with the database, feel free to wipe `unihive.db` to clear out
existing state. This is needed after changes to table schema, etc.