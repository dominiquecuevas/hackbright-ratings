"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/movies')
def show_movies():
    
    return render_template("movies.html")

@app.route('/users')
def user_list():
    """Show list of users."""
    
    users = User.query.all()
    return render_template("user_list.html",
                            users=users)

@app.route("/register", methods=['GET'])
def registration_form():

    email = request.args.get("email")
    password = request.args.get("password")
    return render_template("register_form.html",
                            email=email,
                            password=password)

@app.route("/register", methods=["POST"])
def registration_process():

    email = request.form["email"]
    password = request.form["password"]

    if User.query.filter(User.email == email).first():
        return redirect("/")
    else:
        #create new user in database\
        #redirect
        user = User(email=email,
                    password=password)
        db.session.add(user)
        
        db.session.commit()

    return redirect("/")

@app.route("/login", methods=['GET'])
def login_form():

    email = request.args.get("email")
    password = request.args.get("password")
    return render_template("login_form.html",
                            email=email,
                            password=password)

@app.route("/login", methods=['POST'])
def handle_login():

    email = request.form['email']
    password = request.form['password']

    q = User.query.filter(User.email == email, User.password == password).first()


    if q:
        
        session['curent user_id'] = q.user_id
        flash("Logged in")
    
    return redirect("/")

@app.route("/users/<int:user.user_id>")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
