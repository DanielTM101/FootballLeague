import sqlite3
import unittest
import requests

# Function to fetch Premier League standings from SERP API
def fetch_premier_league_standings(api_key):
    url = f"https://serpapi.com/search.json?q=premier+league+standings&location=austin,+texas,+united+states&api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("sports_results", {}).get("league", {}).get("standings", [])
    except Exception as e:
        print("Error:", e)
        return []

# Function to create the SQLite database and insert Premier League standings
def create_and_insert_data(standings_data):
    if standings_data:
        conn = sqlite3.connect("standings.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS standings (team_name TEXT, points INT)")

        for standing in standings_data:
            team_name = standing["team"]["name"]
            points = int(standing["pts"])

            cursor.execute("INSERT INTO standings VALUES (?, ?)", (team_name, points))

        conn.commit()
        conn.close()

# Function to retrieve and print the Premier League standings table 
def print_premier_league_standings_table():
    conn = sqlite3.connect("standings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM standings ORDER BY points DESC LIMIT 5 ")  
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("Premier League Standings :")
        print("------------------------")
        for row in rows:
            team_name, points = row
            print(f"{team_name} | Points: {points}")
    else:
        print("Premier League Standings table is empty.")

# Function to check if the standings table is empty
def is_standings_table_empty():
    conn = sqlite3.connect("standings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM standings")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0


if __name__ == "__main__":
    api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"

    # Fetch Premier League standings
    standings_data = fetch_premier_league_standings(api_key)

    # Create and insert Premier League standings into SQLite database
    create_and_insert_data(standings_data)

    # Print the Premier League standings table (Top 5)
    print_premier_league_standings_table()


class TestStandingsTable(unittest.TestCase):
    def test_standings_table_not_empty(self):
        result = is_standings_table_empty()
        self.assertFalse(result, "Standings table is empty.")


if __name__ == '__main__':
    unittest.main()