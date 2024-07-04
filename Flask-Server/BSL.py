import requests
from pprint import pprint
import json 
import boto3
from datetime import datetime


# Your API key (replace with your actual API key)
api_key = '5bf985242e9269a130b7b3652bedf297'

# The endpoint URL
url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'
sports = []
json_data = []

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
        sports.append({"key":item['key'], "outrights": item["has_outrights"]})
    
    for x in sports:
        if x["outrights"] == True:
            odds_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/odds/?apiKey={api_key}&regions=us&oddsFormat=american&markets=outrights'
        else:
            event_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/events/?apiKey={api_key}'
            odds_url = f'https://api.the-odds-api.com/v4/sports/{x["key"]}/odds/?apiKey={api_key}&regions=us&markets=h2h,spreads&oddsFormat=american'
        
        try:
            event_response = requests.get(event_url)
            event_response.raise_for_status()  # Raise an exception for HTTP errors
            events_data = event_response.json()
            
            odds_response = requests.get(odds_url)
            odds_response.raise_for_status()  # Raise an exception for HTTP errors
            odds_data = odds_response.json()
            for z in events_data:
                ID = z['id']

                for y in odds_data:
                    if ID == y["id"]:
                        data_set = {
                            "id": ID,
                            'key': x["key"],
                            'title': z["sport_title"],
                            'home': z["home_team"],
                            'away': z["away_team"],
                            'time': z["commence_time"],
                            'markets': y["bookmakers"],
                        }
                        json_data.append(data_set)            
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for {x}: {e}")
else:
    print(f"Error")


#Adding the searching logic for specific sport/team/current Events (Input logic going to change when front-end added)
game_td = input("Please Enter Searching Logic-:")
if(game_td.lower() == "sport"):
    for y in json_data:
        print(y['title'])

    name_sport = input("Please Enter Sport Name from the name of sports above-: ")

    for x in json_data:
        if(name_sport in x['title']):
            print("Home Team -:" + x['home'])
            print("Away Team -:" + x['away'])
            print("Time -:" + x['time'])
            print("Market -:", x['markets'])
    
if(game_td.lower() == "date"):
    c = datetime.now()
    c = c.date()
    for x in json_data:
        commence_datetime_str = x['time']  # Assuming 'time' is in 'YYYY-MM-DD' format
        commence_datetime = datetime.strptime(commence_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        # Extract the date part from commence_datetime
        commence_date = commence_datetime.date()
        if(c == commence_date):
            print("Home Team -:" + x['home'])
            print("Away Team -:" + x['away'])
            print("Time -:" + x['time'])
            print("Market -:", x['markets'])
    
if(game_td.lower() == "team"):
    name_team = input("Please Enter youre team name")
    for x in json_data:
        if(name_team == x['home'] or name_team == x['away']):
            print("Home Team -:" + x['home'])
            print("Away Team -:" + x['away'])
            print("Time -:" + x['time'])
            print("Market -:", x['markets'])
    




