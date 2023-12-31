from flask import Flask, g, render_template, redirect, session, flash, Markup, request
from models import Read_Books, db, connect_db, User, Readlist, Readlist_Books, Shared_Readlist
from forms import RegisterForm, LoginForm, CreateNewReadlistForm
import requests
from sqlalchemy.exc import IntegrityError ### for handling SQLA issues within WTForms
from key import API_KEY
from string import ascii_letters
from random import choice
import urllib.parse

# mapping the base URL of the API into a variable
BASE_URL = "https://www.googleapis.com/books/"

app = Flask(__name__, static_url_path='/static')

# configuring Flask and SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/myreads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "NotTheRealPassword:)"

# connecting to  database
connect_db(app)

@app.route('/')
def hello():
    return render_template('/home.html')

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
        except IntegrityError as e:
            print(e)
            # Appends the errors into the form error field
            form.username.errors.append('Username taken.  Please pick another')
            # Will redirect user back to the same page and have user try again
            return render_template('user/register.html', form=form)

        # Once the commit is successful, adding the newly created user into session["curr_user"]
        do_login(new_user)

        # Flashing a message to the user
        flash('Successfully Created Your Account! Welcome to MyReads!', "success")
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

# Logout route logic
@app.route('/logout')
def logout_user():
    """Logout logc. Will remove the curr_user from the session if it exists. GET requests only."""

    # Making sure only logged in users can logout
    if "curr_user" not in session:
        # Flashes a message if you are not logged in. This is to catch manual typers. Logout page is not present in the UI for guest visitors.
        flash("Please login first!", "danger")
        # Redirects to login page
        return redirect('/login')
    
    # If the user is logged in, calling the method and removing the user from the session
    do_logout()
    # Flashing a message below to the user
    flash("Goodbye! We will miss you!", "info")
    # Redirecting to homepage
    return redirect('/')


@app.route('/search/<string:q>', methods=['GET'])
def show_search_results(q):
    """Logic for sending an API request and displaying the JSON response as an HTML. Expects a GET request."""
    q = urllib.parse.quote(q)
    # sending a GET request to the URL with the query passed to this method. then mapping the results into a variable
    results = requests.get(f"{BASE_URL}v1/volumes", params={"q": q})
    
    # Using try/except to catch any errors that might occur while sending a request to API. Such as sending empty string, space, multiple spaces, unsupported character, etc.
    try:
        # rendering a template and passing the json version of the result
        return render_template('book/search_results.html', results = results.json(), search_term=q)
    # if an exception is generated
    except Exception as e:
        print(e)
        # Flash an error
        flash("Search criteria did not return any results. Please try searching again with a different keyword.", "warning")
        # Redirect to homepage
        return redirect('/')

@app.route('/book/<string:id>')
def show_book_details(id):
    """For displaying information about the individual book. Not a list. GET request only."""
    
    # getting the book information from API and storing into variable
    book = requests.get(f"{BASE_URL}v1/volumes/{id}")

    # only pulling read if the user is logged in
    if "curr_user" in session:
        # getting read books so we can determine if this book has been marked as watched already
        read_books = [x.book_id for x in g.user.read_books]
        book = book.json()
        des =[]
        if 'description' in book['volumeInfo']:
            des = Markup(dict(book['volumeInfo'])['description'])
        # rendering a template and passing the json version of the results, also passing the genres and the page number
        return render_template('book/details.html', book = book, book_read = id in read_books, des = des)
    
    # If the user is not logged in, just passing the book info and the genres. Not passing watched books.
    book = book.json()
    des =[]
    if 'description' in book['volumeInfo']:
        des = Markup(dict(book['volumeInfo'])['description'])
    return render_template('book/details.html', book = book, des = des)

# logic for marking as read or unread
@app.route('/read_unread', methods=['PATCH'])
def mark_umark_watched():
    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    r_id = request.json['book_id']
    # Getting a operation from the payload sent to our API logic
    operation = request.json['oper']
    
    # for read operation
    if operation == "r": 
        # Creating a new instance of the Read_books
        r = Read_Books(user_id=g.user.id, book_id=r_id)
        db.session.add(r)
        db.session.commit()
        return "Successfully marked as read."

    # If the operation is unread,
    elif operation == "u":
        r_id = request.json['book_id']
        for i in g.user.read_books:
            if i.book_id == r_id:
                ur = Read_Books.query.get_or_404(i.id)
                db.session.delete(ur)
                db.session.commit()
                return "Successfully marked as not read."
    else:
        return "Error! Server could not understand your request."
    
@app.route('/readlist/read')
def show_readlist_read():
    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    read_book_ids = [x.book_id for x in g.user.read_books]
    read_books = []
    for id in read_book_ids:
        res = requests.get(f"{BASE_URL}v1/volumes/{id}")
        read_books.append(res)
    return render_template('/readlist/read.html', read_books=read_books)

# Create new readlist logic
@app.route('/readlist/create', methods=['GET','POST'])
def create_new_readlist():

    form = CreateNewReadlistForm()

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    if form.validate_on_submit():
        readlist_name = form.name.data
        
        new_readlist = Readlist(name=readlist_name, user_id=g.user.id)
        db.session.add(new_readlist)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Error. Please try again with different readlist name')
            return render_template('/readlist/create_new.html', form=form)

        flash('Successfully created new readlist!', "success")
        return redirect('/readlist/private')

    return render_template('/readlist/create_new.html', form=form)

@app.route('/readlist/delete', methods=['DELETE'])
def delete_readlist():

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    rlist_id = int(request.json['rlist_id'])
    rlist = Readlist.query.get_or_404(rlist_id)

    if g.user.id != rlist.user_id:
        return "You are not authorized to access this resource!"

    db.session.delete(rlist)
    db.session.commit()
    return "Successfully deleted a readlist."

@app.route('/readlist/add_remove', methods=['PATCH'])
def add_book_to_readlist():

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    book_id = request.json['book_id']
    rlist_id = request.json['rlist_id']

    pm = Readlist_Books(readlist_id = rlist_id, book_id = book_id)
    
    db.session.add(pm)
    db.session.commit()

    return "Successfully added to readlist."

# Remove book from readlist
@app.route('/readlist/add_remove', methods=['DELETE'])
def remove_book_from_readlist():

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
       
    book_id = request.json['book_id']
    rlist_id = int(request.json['rlist_id'])

    pm = Readlist_Books.query.filter_by(readlist_id=rlist_id, book_id=book_id).first()

    rlist = Readlist.query.get_or_404(rlist_id)

    if g.user.id != rlist.user_id:
        return "You are not authorized to access this resource!"
    
    db.session.delete(pm)
    db.session.commit()

    return "Successfully removed from readlist."

# Show list of private readlists on a page
@app.route('/readlist/private')
def show_private_readlists():

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    return render_template('readlist/private_list.html')

# Show details of an individual private readlist
@app.route('/readlist/private/<int:id>')
def show_private_readlist_details(id):

    p = Readlist.query.get_or_404(id)
    
    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    elif g.user.id != p.user_id:
        flash("You are not authorized to access this resource!", "danger")
        return redirect('/login')

    p_book_ids = [x.book_id for x in p.books]
    p_books = []

    for id in p_book_ids:
        # sending a GET request to the API and getting the book details in JSON format
        # appending each book details into the list variable
        p_books.append(requests.get(f"{BASE_URL}v1/volumes/{id}").json())

    return render_template('readlist/private_single.html', readlist = p, readlist_books = p_books)

# Share a private readlist
@app.route('/readlist/share', methods=['PUT'])
def share_private_readlist():
    #Logic for generating a random hash and adding a private readlist into shared readlist table. Expects a PUT request
    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    rlist_id = int(request.json['rlist_id'])

    # Logic for generating a random 10 character url from lowercase and uppercase alphabet    
    letters = ascii_letters # from string library. will print a-z lowercase and A-Z uppercase letters.
    url = (''.join(choice(letters) for i in range(10))) # picks a random sequence of 10 chars

    # creating a new instance of the Shared_Readlist object and passing the readlist id, user id and the newly generated URL
    sp = Shared_Readlist(readlist_id=rlist_id, user_id=g.user.id, url_code=url)

    db.session.add(sp)
    db.session.commit()
    
    return url

# Show a list of shared readlists
@app.route('/readlist/shared', methods=['GET'])
def show_shared_readlists():
    #Logic for displaying all the shared readlists on 1 page. GET request only."""

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    return render_template('readlist/shared_list.html')

# Logic for un-sharing an already shared readlist
@app.route('/readlist/shared', methods=['DELETE'])
def un_share_private_readlist():
    # deleting a shared readlist. The private readlist itself will stay. Expects a DELETE request.

    if "curr_user" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    rlist_id = int(request.json['rlist_id'])

    # finding a first item in the Shared_Readlist object/table that has the correct readlist id
    p = Shared_Readlist.query.filter_by(readlist_id = rlist_id).first()

    db.session.delete(p)
    db.session.commit()

    return "Successfully un-shared a shared readlist."

# Show details of a shared private readlist
@app.route('/readlist/shared/<string:url_code>')
def show_shared_readlist_details(url_code):
    """Logic for querying the DB for the URL provide and showing details of a shared readlist.
    This option is available to everyone. Not only to logged in users.
    """

    sp = Shared_Readlist.query.filter_by(url_code=url_code).first()

    p = sp.readlist

    # Getting the book ids and putting them into a variable
    p_book_ids = [x.book_id for x in p.books]
    p_books = []

    for id in p_book_ids:
        # querying the API for the book details for each book id in the readlist
        p_books.append(requests.get(f"{BASE_URL}v1/volumes/{id}", params={"key": API_KEY}).json())

    a = User.query.get_or_404(p.user_id)

    return render_template('readlist/shared_single_ext.html', readlist=p, books=p_books, author=a)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(debug=True)