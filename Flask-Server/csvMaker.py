import requests
from pprint import pprint
import json 
import boto3
from datetime import datetime
import csv


# Your API key (replace with your actual API key)
api_key = '3ce6dcb618097e653b0b4c0276c8b5c9'

# The endpoint URL
url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'
sports = []
json_data = []
away_team_win = 0
home_team_win = 0
home_team_score = 0
away_team_score = 0

# Getting Region
my_session = boto3.session.Session()
my_region = my_session.region_name
print(f"AWS region: {my_region}")

# Making a GET request to the API
response = requests.get(url)

# Checking if the request was successful
if response.status_code == 200:
    # Parsing the JSON response
    data = response.json()
    for item in data:
        sports.append({"key": item['key'], "outrights": item["has_outrights"]})
    
    for x in sports:
        if x["outrights"]:
            odds_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/odds/?apiKey={api_key}&regions=us&oddsFormat=american&markets=outrights'
        else:
            event_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/events/?apiKey={api_key}'
            odds_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/odds/?apiKey={api_key}&regions=us&markets=h2h,spreads&oddsFormat=american'
            score_url = f'https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?daysFrom=1&apiKey={api_key}'
        
        try:
            event_response = requests.get(event_url)
            event_response.raise_for_status()  # Raise an exception for HTTP errors
            events_data = event_response.json()
            
            odds_response = requests.get(odds_url)
            odds_response.raise_for_status()  # Raise an exception for HTTP errors
            odds_data = odds_response.json()

            score_response = requests.get(score_url)
            score_response.raise_for_status()  # Raise an exception for HTTP errors
            score_data = score_response.json()
            
            for z in events_data:
                ID = z['id']
                home_team_price = None
                away_team_price = None
                home_team_spread = None
                away_team_spread = None
                home_team_spread_price = None
                away_team_spread_price = None
                for y in odds_data:
                    if ID == y["id"]:

                        # Getting BookMaker, and all bookmaker Information
                        bookmakers = y['bookmakers']
                        for bookmaker in bookmakers:
                            for market in bookmaker['markets']:
                                if market['key'] == 'h2h':
                                    for outcome in market['outcomes']:
                                        if outcome['name'] == z['home_team']:
                                            home_team_price = outcome['price']
                                        elif outcome['name'] == z['away_team']:
                                            away_team_price = outcome['price']
                                elif market['key'] == 'spreads':
                                    for outcome in market['outcomes']:
                                        if outcome['name'] == z['home_team']:
                                            home_team_spread = outcome['point']
                                            home_team_spread_price = outcome['price']
                                        elif outcome['name'] == z['away_team']:
                                            away_team_spread = outcome['point']
                                            away_team_spread_price = outcome['price']
                            data_set = {
                                'id': ID,
                                'key': x["key"],
                                'title': z["sport_title"],
                                'time': z["commence_time"],
                                'home': z["home_team"],
                                'away': z["away_team"],
                                "home_team_price": home_team_price,
                                "away_team_price": away_team_price,
                                "home_team_spread": home_team_spread,
                                "away_team_spread": away_team_spread,
                                "home_team_spread_price": home_team_spread_price,
                                "away_team_spread_price": away_team_spread_price,
                                "bookmaker": bookmaker['title'],
                                "last_update": bookmaker['last_update']
                            }
                            json_data.append(data_set)            
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for {x}: {e}")
else:
    print("Error fetching sports data")


#Convering JSON To Csv
keys_array = [
    'id',
    'key',
    'title',
    'time',
    'home',
    'away',
    'home_team_price',
    'away_team_price',
    'home_team_spread',
    'away_team_spread',
    'home_team_spread_price',
    'away_team_spread_price',
    'bookmaker',
    'last_update'
]


with open("TrainingMode.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = keys_array) 
    writer.writeheader() 
    writer.writerows(json_data) 


# Output the collected data
# pprint(json_data)
