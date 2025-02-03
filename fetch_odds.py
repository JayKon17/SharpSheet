import requests
import json
from datetime import datetime, timedelta

# Read API key from file
with open("api_key.txt", "r") as file:
    API_KEY = file.read().strip()

# Define league ID
league_ID = "NBA"

# API URL
URL = f'https://api.sportsgameodds.com/v1/odds/?leagueID={league_ID}&region=us'

# Headers
headers = {'X-Api-Key': API_KEY}

# Get current time
current_time = datetime.now()
today = current_time.date()
tomorrow = today + timedelta(days=1)

# Fetch data
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()

        # Print the full data structure for debugging (optional)
        print(json.dumps(data, indent=4))  

        # Extract relevant game data
        cleaned_data = []

        # Check if the key 'odds' exists in the response
        if 'odds' not in data:
            print("Error: 'odds' key is missing in the response data.")
        else:
            for game in data['odds']:
                try:
                    # Extract the time and ensure it matches today's or tomorrow's date
                    game_time = datetime.strptime(game['commence_time'], '%Y-%m-%d %H:%M:%S')

                    # Only keep games that are today or tomorrow
                    if (game_time.date() == today and game_time > current_time) or game_time.date() == tomorrow:
                        game_info = {
                            "matchup": game.get("matchup", "Unknown"),
                            "game_time": game_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "odds": []
                        }

                        # Handle the betting markets and filter for team-related bets
                        if 'bettingMarkets' in game:
                            for key, bet in game['bettingMarkets'].items():
                                if bet.get("statEntityID") == "all":  # Only keep team-related bets
                                    game_info["odds"].append({
                                        "period": bet.get("periodID", "Unknown"),
                                        "type": bet.get("betTypeID", "Unknown"),
                                        "side": bet.get("sideID", "Unknown"),
                                        "bookmaker": bet.get("bookmaker", "Unknown"),
                                        "book_odds": bet.get("bookOdds", "Unknown"),
                                        "over_under": bet.get("bookOverUnder", None),
                                        "score": bet.get("score", None)
                                    })

                        cleaned_data.append(game_info)

                except KeyError as e:
                    print(f"KeyError while processing game: {e}")
                    continue

            # Save the cleaned data if there were any games processed
            if cleaned_data:
                with open('cleaned_nba_odds.json', 'w') as json_file:
                    json.dump(cleaned_data, json_file, indent=4)

                print(f"Saved {len(cleaned_data)} cleaned NBA games to cleaned_nba_odds.json")
            else:
                print("No games were found for today or tomorrow.")
                
    except (ValueError, KeyError) as e:
        print(f"Error parsing the response data: {e}")
else:
    print(f"Error fetching data: {response.status_code} - {response.text}")
