import sqlite3
import requests
<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
import unittest

app = Flask(__name__)

#mock database
users = {
    "existing_user": "existing_password"
}

=======
>>>>>>> d610682996b32821c024ae96e5949792f1c176e0

# Function to fetch team information from SERP API
def fetch_team_info(team_name, league, api_key):
    url = f"https://serpapi.com/search.json?q={team_name}+{league}&location=austin,+texas,+united+states&api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
<<<<<<< HEAD
        
        # Check if the API returned any relevant data
        if "sports_results" not in data:
            return {}

        sports_results = data["sports_results"]

        # Check if the sports_results contain the required data
        if "rankings" not in sports_results or "games" not in sports_results:
=======
        sports_results = data.get("sports_results", {})
        if not sports_results:
            print(f"No information available for {team_name}.")
>>>>>>> d610682996b32821c024ae96e5949792f1c176e0
            return {}

        team_info = {
            "team_name": team_name,
<<<<<<< HEAD
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



# Function to create the SQLite database and insert team info
def create_and_insert_team_data(team_name, rankings, games):
    db_file = "teams_info.db"
=======
            "rankings": sports_results.get("rankings", ""),
            "games": sports_results.get("games", [])
        }
        return team_info
    except Exception as e:
        print("Error:", e)
        return {}

# Function to create the SQLite database and insert team info
def create_and_insert_data(team_name, rankings, games):
    db_file = f"{team_name.lower()}_info.db"
>>>>>>> d610682996b32821c024ae96e5949792f1c176e0
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teams (team_name TEXT, rankings TEXT, games TEXT)")

        cursor.execute("INSERT INTO teams (team_name, rankings, games) VALUES (?, ?, ?)", (team_name, rankings, str(games)))

<<<<<<< HEAD
# Function to create the SQLite database and insert user info
def create_and_insert_user_data(username, password):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

# Function to create the SQLite database and insert user's picked teams
def create_and_insert_user_teams(username, football_team, mlb_team):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_teams (username TEXT, football_team TEXT, mlb_team TEXT)")

        cursor.execute("INSERT INTO user_teams (username, football_team, mlb_team) VALUES (?, ?, ?)", (username, football_team, mlb_team))


def is_user_exists(username):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone() is not None

# Function to retrieve and print team info
def print_teams_info(team_name):
    db_file = "teams_info.db"
=======
# Function to retrieve and print team info
def print_teams_info(team_name):
    db_file = f"{team_name.lower()}_info.db"
>>>>>>> d610682996b32821c024ae96e5949792f1c176e0
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams")
        rows = cursor.fetchall()

        if rows:
            print("Team Information:")
            print("-----------------")
            for row in rows:
                team_name, rankings, games = row
                print(f"Team: {team_name}")
                print(f"Rankings: {rankings}")
                print("Games:")
                for game in eval(games):
                    date = game.get('date', '')
                    teams = game.get('teams', [])

                    teams_str = ' vs '.join(team['name'] for team in teams)
                    print(f"  Date: {date}")
                    print(f"  Teams: {teams_str}")
                    print("-----------------")
        else:
            print("No team information available in the database.")

<<<<<<< HEAD
def authenticate_user(username, password):
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data is not None:
            saved_username, saved_password = user_data
            if saved_password == password:
                return True

    return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]

        if action == "login":
            return redirect(url_for("login"))
        elif action == "signup":
            return redirect(url_for("signup"))

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login request
        username = request.form["username"]
        password = request.form["password"]
        if authenticate_user(username, password):
            return redirect(url_for("show_teams", username=username))
        else:
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle sign-up request
        username = request.form["username"]
        password = request.form["password"]

        # Fetch inputs for a football team and MLB team
        football_team_input = request.form["football_team"]
        mlb_team_input = request.form["mlb_team"]

        # Fetch information for the football team
        football_team_info = fetch_team_info(football_team_input, "Premier League", api_key)
        if not football_team_info:
            return render_template("signup.html", message="Invalid football team. Please try again with a team from the Premier League.")

        # Fetch information for the MLB team
        mlb_team_info = fetch_team_info(mlb_team_input, "MLB", api_key)
        if not mlb_team_info:
            return render_template("signup.html", message="Invalid MLB team. Please try again with a valid MLB team.")

        if not is_user_exists(username):
            create_and_insert_user_data(username, password)

            # Create and insert user's picked teams into the SQLite database
            create_and_insert_user_teams(username, football_team_info["team_name"], mlb_team_info["team_name"])

            return redirect(url_for("login", message="Signup successful. Please login with your new account."))
        else:
            return render_template("signup.html", message="Username already exists. Please choose a different username.")

    return render_template("signup.html")


@app.route("/dashboard/<username>", endpoint="show_teams")
def dashboard(username):
    # Fetch user's picked teams
    db_file = "users_info.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT football_team, mlb_team FROM user_teams WHERE username=?", (username,))
        user_teams = cursor.fetchone()

        if user_teams is not None:
            football_team, mlb_team = user_teams

            # Print team info from the databases
            football_team_info = fetch_team_info(football_team, "Premier League", api_key)
            mlb_team_info = fetch_team_info(mlb_team, "MLB", api_key)

            return render_template("dashboard.html", username=username, football_team=football_team_info, mlb_team=mlb_team_info)
        else:
            return "No team information available. Please pick teams first."

""" Include test cases in the same file
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
    #unittest.main()
=======
if __name__ == "__main__":
    api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"

    # Get inputs for a football team and MLB team
    football_team_input = input("Enter the name of a football team: ")
    mlb_team_input = input("Enter the name of an MLB team: ")

    # Fetch information for the football team
    football_team_info = fetch_team_info(football_team_input, "Premier League", api_key)

    # Fetch information for the MLB team
    mlb_team_info = fetch_team_info(mlb_team_input, "MLB", api_key)

    # Create and insert team info into SQLite databases
    create_and_insert_data(football_team_info["team_name"], football_team_info["rankings"], football_team_info["games"])
    create_and_insert_data(mlb_team_info["team_name"], mlb_team_info["rankings"], mlb_team_info["games"])

    # Print team info from the databases
    print_teams_info(football_team_info["team_name"])
    print_teams_info(mlb_team_info["team_name"])
>>>>>>> d610682996b32821c024ae96e5949792f1c176e0
