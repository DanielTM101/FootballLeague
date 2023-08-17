import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for
#import unittest

app = Flask(__name__)

db_file = "users_info.db"
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, football_team TEXT, mlb_team TEXT)")

# Function to fetch team information from SERP API
def fetch_team_info(team_name, league, api_key):
    url = f"https://serpapi.com/search.json?q={team_name}+{league}&location=austin,+texas,+united+states&api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "sports_results" not in data:
            return {}

        sports_results = data["sports_results"]

        if "rankings" not in sports_results or "games" not in sports_results:
            return {}

        team_info = {
            "team_name": team_name,
            "rankings": sports_results["rankings"],
            "games": sports_results["games"]
        }
        return team_info
    except requests.exceptions.HTTPError as e:
        return {}
    except requests.exceptions.RequestException as e:
        return {}
    except Exception as e:
        return {}

# Function to create the SQLite database and insert user info
def create_and_insert_user_data(username, password, football_team, mlb_team):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE username=?", (username,))
        existing_username = cursor.fetchone()
        if existing_username:
            return "Username already exists. Please choose a different username."

        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, football_team TEXT, mlb_team TEXT)")

        cursor.execute("INSERT INTO users (username, password, football_team, mlb_team) VALUES (?, ?, ?, ?)",
                       (username, password, football_team, mlb_team))
        return None

def authenticate_user(username, password):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, football_team, mlb_team FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data is not None:
            saved_username, saved_password, football_team, mlb_team = user_data
            if saved_password == password:
                return True, football_team, mlb_team
    return False, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        auth_status, football_team, mlb_team = authenticate_user(username, password)
        if auth_status:
            return redirect(url_for("show_teams", username=username, football_team=football_team, mlb_team=mlb_team))
        else:
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        football_team_input = request.form["football_team"]
        mlb_team_input = request.form["mlb_team"]
        
        football_team_info = fetch_team_info(football_team_input, "Premier League", api_key)
        if not football_team_info:
            return render_template("signup.html", message="Invalid football team. Please try again with a team from the Premier League.")

        mlb_team_info = fetch_team_info(mlb_team_input, "MLB", api_key)
        if not mlb_team_info:
            return render_template("signup.html", message="Invalid MLB team. Please try again with a valid MLB team.")

        error_message = create_and_insert_user_data(username, password, football_team_info["team_name"], mlb_team_info["team_name"])
        if error_message:
            return render_template("signup.html", message=error_message)

        return redirect(url_for("login", message="Signup successful. Please login with your new account."))

    return render_template("signup.html")

@app.route("/dashboard/<username>/<football_team>/<mlb_team>", endpoint="show_teams")
def dashboard(username, football_team, mlb_team):
    football_team_info = fetch_team_info(football_team, "Premier League", api_key)
    mlb_team_info = fetch_team_info(mlb_team, "MLB", api_key)

    return render_template("dashboard.html", username=username, football_team=football_team_info, mlb_team=mlb_team_info)

""" 
class TestTeamInfo(unittest.TestCase):
    def test_fetch_team_info_valid_team(self):
        # Test fetching valid team info from the API for a generic team name in the Premier League
        team_name = "Arsenal"
        league = "Premier League"
        api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"
        team_info = fetch_team_info(team_name, league, api_key)
        self.assertTrue(team_info, "Valid team info should be retrieved for a generic team in the Premier League.")

    def test_fetch_team_info_invalid_team(self):
        # Test fetching invalid team info from the API for an unknown team name in Premier League
        team_name = "Invalid Team Name"
        league = "Premier League"
        api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"
        team_info = fetch_team_info(team_name, league, api_key)
        self.assertFalse(team_info, "Invalid team info should not be retrieved for an unknown team name in Premier League.")

    def test_fetch_team_info_valid_mlb_team(self):
        # Test fetching valid team info from the API for a generic team name in MLB
        team_name = "New York Yankees"
        league = "MLB"
        api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"
        team_info = fetch_team_info(team_name, league, api_key)
        self.assertTrue(team_info, "Valid team info should be retrieved for a generic team in MLB.")

    def test_fetch_team_info_invalid_mlb_team(self):
        # Test fetching invalid team info from the API for an unknown team name in MLB
        team_name = "Invalid Team Name"
        league = "MLB"
        api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"
        team_info = fetch_team_info(team_name, league, api_key)
        self.assertFalse(team_info, "Invalid team info should not be retrieved for an unknown team name in MLB.")

    def test_is_user_exists_existing(self):
        # Test if an existing username is detected
        existing_username = "bob"
        self.assertTrue(is_user_exists(existing_username), "Existing user should be detected.")

    def test_is_user_exists_new(self):
        # Test if a new username is not detected
        new_username = "new_user"
        self.assertFalse(is_user_exists(new_username), "New user should not be detected.")"""

if __name__ == "__main__":
    api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"
    app.run(debug=True)
