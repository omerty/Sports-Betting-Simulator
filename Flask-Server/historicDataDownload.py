import requests
import json
from datetime import datetime, timedelta
import random

api_key_paid = 'ecb83721e958582dac3a4e7198433b11'

football_keys = [
    "americanfootball_cfl",
    "americanfootball_ncaaf",
    "americanfootball_nfl",
    "americanfootball_ufl",
]

soccer_keys = [
    "soccer_fifa_world_cup",
    "soccer_fifa_world_cup_womens",
    "soccer_fifa_world_cup_winner",
    "soccer_usa_mls",
]

hockey_keys = [
    "icehockey_nhl"
]

def random_date_in_past_two_years():
    today = datetime.now()
    start_date = today - timedelta(days=2*365)
    random_days = random.randint(0, 2*365)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')

# Maximum number of events to fetch per sport
max_events_per_sport = 5

def fetch_events(sport):
    events_collected_tried = 0
    sport_historical_odds = []

    while events_collected_tried < max_events_per_sport:
        random_date = random_date_in_past_two_years()
        endpoint = f'https://api.the-odds-api.com/v4/sports/{sport}/odds?apiKey={api_key_paid}&regions=us&marketsplayer_points,h2h_q1&date={random_date}'

        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            events = response.json()
            
            if events:
                for event in events:
                    sport_historical_odds.append(event)
                    events_collected_tried += 1
            else:
                events_collected_tried += 1
                continue  
            
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred for sport {sport}: {err}")
        except Exception as err:
            print(f"An error occurred for sport {sport}: {err}")
    
    return sport_historical_odds

# Collecting soccer events
soccer_historical_odds = []
for sport in soccer_keys:
    soccer_historical_odds.extend(fetch_events(sport))

output_file = "historical_odds_soccer.json"
with open(output_file, "w") as f:
    json.dump(soccer_historical_odds, f, indent=4)

football_historical_odds = []
for sport in football_keys:
    football_historical_odds.extend(fetch_events(sport))

output_file = "football_historical_odds.json"
with open(output_file, "w") as f:
    json.dump(football_historical_odds, f, indent=4)

hockey_historical_odds = []
for sport in hockey_keys:
    hockey_historical_odds.extend(fetch_events(sport))

output_file = "hockey_historical_odds.json"
with open(output_file, "w") as f:
    json.dump(hockey_historical_odds, f, indent=4)


print(f"All data successfully written to")

