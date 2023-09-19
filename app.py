"""
My system has two kinds of user: regular ones, and administrators.
Choose Register on the main page in order to register as a regular user.
But to login as an administrator, the user name is Admin and the password is Gerrard

Throughout the file there are comments for link attempts , this is where I attempt to link 
the user and events table together so user data is restored when logging back in. My attempts were unsuccessful.
"""


from flask import Flask, g, render_template, request, session, redirect, url_for
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Registrationform, Loginform, Eventform, Dateform, Editform
from functools import wraps


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this-is-my-secret-key" 
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login', next = request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    db = get_db()
    events = db.execute("""SELECT * FROM events
                        WHERE event_id < 7;""").fetchall()
    return render_template("index.html", events = events)

@app.route("/register", methods=["GET","POST"])
def register():
    form = Registrationform()
    if form.validate_on_submit():
        user_id = form.user_id.data 
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id is already taken.")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                    VALUES (?, ?);""",
                    (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form = form )

@app.route("/login", methods=["GET","POST"])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user_id = form.user_id.data 
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users
                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if matching_user is None:
            form.user_id.errors.append("Unknown user id.")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form = form )

@app.route("/logout")
def logout():
    db = get_db()
    db.execute("""DELETE FROM events 
                    WHERE event_id > 6;""")
    db.commit()
    session.clear()
    return redirect( url_for("index") )

@app.route("/events")
@login_required
def events():
    db = get_db()
    events = db.execute("""SELECT * FROM events
                            WHERE event_id < 7;""").fetchall()
    return render_template("index.html", events = events) 

@app.route("/add_event", methods=["GET","POST"])
@login_required
def add_event():
    db = get_db()
    form = Eventform()
    message = ""
    if form.validate_on_submit():
        title = form.title.data
        details = form.details.data
        db.execute("""INSERT INTO events (name, description) 
                        VALUES (?, ?); """, (title, details))
        db.commit()
        message = "New event added"
    return render_template("add_event.html", form = form, message = message)

@app.route("/delete/<int:event_id>")
@login_required
def delete(event_id):
    db = get_db()
    db.execute("""DELETE FROM events 
                    WHERE event_id = ?;""", (event_id,)).fetchone()
    db.commit()
    if session["user_id"] != "Admin":
        return redirect( url_for("user_events") )
    return redirect( url_for("index") )
   
@app.route("/events/<int:event_id>", methods=["GET","POST"])
@login_required
def event(event_id):
    db = get_db()
    event = db.execute("""SELECT * FROM events
                            WHERE event_id = ?;""", (event_id,)).fetchone()
    event_name = event["name"]
    message = ""
    form = Dateform()
    if form.validate_on_submit():
        event_date = form.event_date.data
        event_start = form.event_start.data
        event_starts = str(event_start)
        event_end = form.event_end.data
        event_ends = str(event_end)
        details = form.details.data
        db.execute("""INSERT INTO events (name, date, start_time, end_time, description) 
                        VALUES (?, ?, ?, ?,?);""", (event_name, event_date, event_starts, event_ends, details))
        db.commit()
        message = "New event created"  
    return render_template("event.html", form = form, event = event, message = message) 

@app.route("/calender")
@login_required
def calender():
    # link attempt
    # g.user = session.get("user_id", None)
    # user = g.user
    if "calender" not in session:
        session["calender"] = {}
    event_names = {}
    event_dates = {}
    event_starts = {}
    event_ends = {}
    details = {}
    db = get_db()
    for event_id in session["calender"]:
        # link attempt
        # try: 
        #     event = db.execute("""SELECT * FROM events
        #                 WHERE events.event_id =
        #                 (SELECT user_data.event_id
        #                 FROM events 
        #                 JOIN user_data
        #                 JOIN users 
        #                 ON events.event_id = user_data.event_id
        #                 AND users.user_id = user_data.user_id 
        #                 WHERE users.user_id = ?); """,(user,)).fetchone()
        # except:
        event = db.execute("""SELECT * FROM events
                            WHERE event_id = ?;""",(event_id,)).fetchone()
        event_name = event["name"]
        event_date = event["date"]
        event_start = event["start_time"]
        event_end = event["end_time"]
        event_details = event["description"]
        event_names[event_id] = event_name
        event_dates[event_id] = event_date
        event_starts[event_id] = event_start
        event_ends[event_id] = event_end
        details[event_id] = event_details
    
    return render_template("calender.html", calender = session["calender"], event_names = event_names, event_dates = event_dates, event_starts = event_starts, event_ends = event_ends, details = details) 

@app.route("/add_to_calender/<int:event_id>")
@login_required
def add_to_calender(event_id):

    if "calender" not in session:
        session["calender"] = {}  
    if event_id not in session["calender"]:
        session["calender"][event_id] = 0 
    session["calender"][event_id] = session["calender"][event_id] + 1
    
    return redirect( url_for("calender") )

@app.route("/remove_from_calender/<int:event_id>")
@login_required
def remove_from_calender(event_id):

    if event_id in session["calender"]:
        session["calender"][event_id] = session["calender"][event_id] - 1 
        if session["calender"][event_id] < 1:
            session["calender"].pop(event_id, None) 
    return redirect( url_for("calender") )

@app.route("/user_events")
def user_events():
    message = ""
    db = get_db()
    events = db.execute("""SELECT * FROM events
                            WHERE event_id > 6;""").fetchall()
    user_event = db.execute("""SELECT * FROM user_data;""").fetchall()
    return render_template("user_events.html", events = events, message = message, user_event = user_event) 

@app.route("/edit/<int:event_id>", methods=["GET","POST"])
def edit(event_id):
    db = get_db()
    event = db.execute("""SELECT * FROM events
                            WHERE event_id = ?;""", (event_id,)).fetchone()
    event_name = event["name"]
    message = ""
    form = Editform()
    if form.validate_on_submit():
        event_date = form.event_date.data
        event_start = form.event_start.data
        event_starts = str(event_start)
        event_end = form.event_end.data
        event_ends = str(event_end)
        details = form.details.data
        db.execute("""UPDATE events SET 
                    name = ?, date = ?, start_time = ?, end_time = ?, description = ?
                    WHERE event_id = ?;""", (event_name, event_date, event_starts, event_ends, details, event_id))
        db.commit()
        message = "Event details have been changed."  
    return render_template("event.html", form = form, event = event, message = message) 


# link attempt
# @app.route("/store/<int:event_id>")
# def store(event_id):
#     g.user = session.get("user_id", None)
#     user = g.user
#     db = get_db()
#     db.execute("""INSERT into user_data (event_id)
#                 VALUES event_id
#                 WHERE user_id = ?
#                 AND event_id = ?;""",(user, event_id))
#     db.commit()
#     return redirect( url_for("user_events") )