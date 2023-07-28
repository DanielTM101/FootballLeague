import sqlite3
import requests

# Function to fetch team information from SERP API
def fetch_team_info(team_name, league, api_key):
    url = f"https://serpapi.com/search.json?q={team_name}+{league}&location=austin,+texas,+united+states&api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        sports_results = data.get("sports_results", {})
        if not sports_results:
            print(f"No information available for {team_name}.")
            return {}

        team_info = {
            "team_name": team_name,
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
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teams (team_name TEXT, rankings TEXT, games TEXT)")

        cursor.execute("INSERT INTO teams (team_name, rankings, games) VALUES (?, ?, ?)", (team_name, rankings, str(games)))

# Function to retrieve and print team info
def print_teams_info(team_name):
    db_file = f"{team_name.lower()}_info.db"
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
