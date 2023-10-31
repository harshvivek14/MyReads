from flask import Flask, g, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError ### for handling SQLA issues within WTForms


app = Flask(__name__)

# configuring Flask and SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@localhost/myreads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "NotTheRealPassword:)"

# connecting to  database
connect_db(app)

@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'

@app.route('/home')
def show_home():
    return render_template('/home.html')

@app.before_request
def add_user_to_g():
    """Before any request, if we're logged in, add curr user to Flask global."""

    # if the current user is stored in session cookies
    if "curr_user" in session:
        # set the user object into a global user variable
        g.user = User.query.get(session["curr_user"])

    else:
        # if the cookie is not found, settings the global user variable to None
        g.user = None

def do_login(user):
    """Log in user."""
    # Settings the curr_user cookie variable as the id of the user. user is passed into this method.
    session["curr_user"] = user.id

def do_logout():
    """Logout user."""
    # If the curr_user is stored in the session, delete it. This will log the user out.
    if "curr_user" in session:
        del session["curr_user"]

# Registration route. Accepts GET and POST requests and performs operations based on the REST method received.
@app.route('/register', methods=['GET','POST'])
def register_user():
    """For registration logic. Accepts GET and POST requests"""
    # mapping a registration form into a variable
    form = RegisterForm()

    # for handling POST requests
    if form.validate_on_submit():
        # if the CSRF token has been validated successfully,
        # maps all the data received from the form into variables
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        
        # Calls the register class method inside the User Data Model. The method is stored under models.py. 
        # This method returns the user object.. Creates a new instance of the User object and stored into a variable.
        new_user = User.register(first_name, last_name, username, password)

        # Add the newly created user object into the DB.
        db.session.add(new_user)

        try:
            # Will try to commit the newly created user into the DB.
            db.session.commit()

        # If the commit errors out,
        except IntegrityError:
            # Appends the errors into the form error field
            form.username.errors.append('Username taken.  Please pick another')
            # Will redirect user back to the same page and have user try again
            return render_template('user/register.html', form=form)

        # Once the commit is successful, adding the newly created user into session["curr_user"]
        do_login(new_user)

        # Flashing a message to the user
        flash('Successfully Created Your Account! Welcome to MeKino!', "success")
        # Redirecting to the main page.
        return redirect('/')

    # for handling GET request
    # will render a template and pass the form into it.
    return render_template('user/register.html', form=form)

# Login route logic
@app.route('/login', methods=['GET','POST'])
def login_user():
    """For login logic. Accepts GET and POST requests."""
    # mapping a logic form into a variable
    form = LoginForm()

    # for handling POST requests
    if form.validate_on_submit():
        # if the CSRF token has been validated successfully,
        # maps all the data received from the form into variables
        username = form.username.data
        password = form.password.data

        # Calls the logic class method inside the User Data Model. The method is stored under models.py. 
        # This method returns the user object if the password passed into the method has been validated succesffully.
        user = User.authenticate(username, password)

        # Making sure that the user has been authenticated successfully
        if user:
            # If so, adding the logged in user into session["curr_user"]
            do_login(user)
            # Flashing a message to the user
            flash(f"Welcome Back, {user.username}!", "success")
             # Redirecting to the main page.
            return redirect('/')
        else:
            # If the user hasn't authenticated successfully, show an error in the form.
            # Have the user try again.
            form.username.errors = ['Invalid username and/or password.']

    # for handling GET request
    # will render a template and pass the form into it.
    return render_template('user/login.html', form=form)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()