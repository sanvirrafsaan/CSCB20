from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
# TODO: add secret key for Flask session

EVENT_ID = 1
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
HOURS = list(range(9, 17))


# TODO: 
# connect to the SQLite database file (data.db)
# return connection object
def connect_to_database():
    pass


def get_db():
    conn = connect_to_database()
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# TODO:
# authenticate user with the given username and password
# if valid:
#   store uid and username in a session
#   return True
# otherwise return False
def authenticate_user(conn, username, password):
    pass


# TODO:
# get current user details from the session
# return (uid, username) if logged in, else None
def get_current_user():
    pass


# TODO:
# clear session with user information
# returns nothing
def clear_current_user():
    pass


# TODO:
# delete all availability votes for given uid and eid
# commit the changes
# return nothing
def del_all_votes(conn, uid, eid):
    pass


# TODO:
# insert a vote for given uid, eid, day and hour
# commit the changes
# return nothing
def add_vote(conn, uid, eid, day, hour):
    pass


# TODO:
# return a list of tuples of the form of (day, hour)
# for which the user uid has voted
def get_user_votes(conn, uid, eid):
    pass


def get_event_title(conn, eid):
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT title FROM events WHERE eid = ?;",
        (eid,)
    ).fetchone()
    return row["title"]


def get_voter_names(conn, eid):
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT a.day, a.hour, u.username
        FROM availability a
        JOIN users u ON a.uid = u.uid
        WHERE a.eid = ?
        ORDER BY a.day, a.hour, u.username;
        """,
        (eid,)
    ).fetchall()

    voter_names = {}
    for row in rows:
        key = (row["day"], row["hour"])
        voter_names.setdefault(key, []).append(row["username"])
    return voter_names


@app.route("/", methods=["GET"])
def home():
    if get_current_user():
        return redirect(url_for("schedule"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db()
        valid = authenticate_user(conn, username, password)
        conn.close()

        if valid:
            return redirect(url_for("schedule"))

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html", error=None)


@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        slots_string = request.form.get("slots", "").strip()

        selected = []
        if slots_string:
            for item in slots_string.split(","):
                day, hour = item.split("-")
                hour = int(hour)
                if day in DAYS and hour in HOURS:
                    selected.append((day, hour))

        for day, hour in selected:
            conn = get_db()
            add_vote(conn, user[0], EVENT_ID, day, hour)
            conn.close()

    conn = get_db()
    event_title = get_event_title(conn, EVENT_ID)
    user_votes = get_user_votes(conn, user[0], EVENT_ID)
    has_voted = len(user_votes) > 0

    voter_names = get_voter_names(conn, EVENT_ID) if has_voted else {}
    counts = {k: len(v) for k,v in voter_names.items()}

    max_count = max(counts.values(), default=0)
    conn.close()

    return render_template(
        "schedule.html",
        username=user[1],
        event_title=event_title,
        days=DAYS,
        hours=HOURS,
        has_voted=has_voted,
        user_votes=user_votes,
        counts=counts,
        voter_names=voter_names,
        max_count=max_count
    )


@app.route("/revote", methods=["POST"])
def revote():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    conn = get_db()
    del_all_votes(conn, user[0], EVENT_ID)
    conn.close()

    return redirect(url_for("schedule"))


@app.route("/logout", methods=["POST"])
def logout():
    clear_current_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)