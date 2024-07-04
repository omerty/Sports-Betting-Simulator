
from flask import Flask, request, jsonify, g
import mysql.connector
from mysql.connector import Error
import bcrypt
import re
import dns.resolver
import secrets
import socket
import smtplib
from flask_cors import CORS
import requests
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
CORS(app)

api_key = 'da3c8ebb3604ad55c7146a2e21cee9f4'
database_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'auth_plugin': 'mysql_native_password',
    'database': 'users'
}

sports_keys = {
    'Soccer': [
        "soccer_fifa_world_cup",
        "soccer_fifa_world_cup_womens",
        "soccer_fifa_world_cup_winner",
        "soccer_usa_mls"
    ],
    'Football': ["americanfootball_ncaaf", "americanfootball_nfl"],
    'Cricket': [
        "cricket_big_bash", "cricket_caribbean_premier_league", "cricket_icc_world_cup", "cricket_international_t20", "cricket_ipl", "cricket_odi",
        "cricket_psl", "cricket_t20_blast", "cricket_test_match"
    ],
    'Hockey': ["icehockey_nhl", "icehockey_nhl_championship_winner", "icehockey_sweden_hockey_league", "icehockey_sweden_allsvenskan"]
}

def valid_email(email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return re.fullmatch(email_regex, email) is not None

def domain_validator(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mxRecord = records[0].exchange.to_text()

        host = socket.gethostname()
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(email)
        server.quit()

        return code == 250
    except:
        return False

def db_connection():
    return mysql.connector.connect(**database_config)

@app.before_request
def before_request():
    token = request.headers.get('Authorization')
    print(f"Token received: {token}")  # Debug statement to print the token
    
    if token:
        try:
            # If your token includes the "Bearer " prefix, strip it out
            if token.startswith('Bearer '):
                token = token.split(' ')[1]

            print("Decoding token...")  # Debug statement before decoding
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.email = data.get('email')
            print(f"Decoded email: {g.email}")  # Debug statement to print the decoded email
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            g.email = None
        except jwt.InvalidTokenError:
            app.logger.error('Invalid token')
            g.email = None
        except Exception as e:
            print(f"Token decoding error: {e}")
            g.email = None
    else:
        g.email = None

def token_required(f):
    def wrapper(*args, **kwargs):
        if g.email is None:
            return jsonify({'error': 'Token is missing or invalid'}), 403
        return f(*args, **kwargs)
    return wrapper

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if not valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not domain_validator(email):
        return jsonify({'error': 'Invalid email domain'}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            bets JSON,
            coins INT NOT NULL DEFAULT 1000
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bets (
            user_email VARCHAR(255) NOT NULL,
            game_id VARCHAR(255) NOT NULL,
            bet_details VARCHAR(255) NOT NULL,
            bet_amount INT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
        """)
        
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email address already exists'}), 400

        # Insert a new user with empty bets array and 1000 coins
        cursor.execute("INSERT INTO users (email, password, bets) VALUES (%s, %s, %s)", (email, password_hash.decode('utf-8'), '[]'))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            token = generate_token(email)  # Generate token function
            g.email = email
            print("print -> ", email)
            return jsonify({'message': 'Login successful', 'token': token, 'email': email}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 400

    except Exception as e:
        print("HERE")
        return jsonify({'error': str(e)}), 500

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

def generate_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def fetch_events(sport_key):
    url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/events?apiKey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching events for {sport_key}: {response.status_code}")
        return None
    
    events = []
    for event in response.json():
        try:
            newUrl = f'https://api.the-odds-api.com/v4/sports/{sport_key}/events/{event["id"]}/odds?apiKey={api_key}&regions=us&oddsFormat=american'
            newResponse = requests.get(newUrl)
            if newResponse.status_code != 200:
                print(f"Error fetching odds for event {event['id']}: {newResponse.status_code}")
                continue
            returned_data = newResponse.json()
            
            event_odds = []
            for bookmaker in returned_data.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    if market.get("key") == "h2h": 
                        event_odds.extend(market.get("outcomes", []))
            
            date_obj = datetime.strptime(event["commence_time"], "%Y-%m-%dT%H:%M:%SZ")
            events.append({
                "event_id" : event["id"],
                "home_team": event["home_team"],
                "away_team": event['away_team'],
                "commence_time": event["commence_time"],
                "event_odds": event_odds
            })
        except KeyError as e:
            print(f"KeyError: {e} for event {event}")
        except Exception as e:
            print(f"Exception: {e} for event {event}")
    
    return events

def get_events(sport):
    currentDate = datetime.now()
    maxDate = currentDate + timedelta(days=7)
    date_filter = lambda date_obj: currentDate <= date_obj <= maxDate

    events = []
    for sport_key in sports_keys[sport]:
        sport_events = fetch_events(sport_key)
        if sport_events is not None:
            filtered_events = [event for event in sport_events if date_filter(datetime.strptime(event["commence_time"], "%Y-%m-%dT%H:%M:%SZ"))]
            events.extend(filtered_events)
    return events

@app.route('/api/<sport>', methods=['GET'])
def get_sport_events(sport):
    if sport not in sports_keys:
        return jsonify({'error': 'Sport not supported'}), 400

    events = get_events(sport)
    if not events:
        return jsonify({'message': 'No events found'}), 404
    return jsonify(events), 200

@app.route('/placeBet', methods=['POST'])
@token_required
def save_bet():
    data = request.get_json()
    betAmount = data.get('betAmount')
    selectedBetOption = data.get('selectedBetOption')
    eventId = 1234543234
    email = g.email
    
    if not email or not betAmount or not selectedBetOption:
        return jsonify({'error': 'Email, bet amount, and selected bet option are required'}), 400
    
    try:
        betAmount = int(betAmount)
        if betAmount <= 0:
            return jsonify({'error': 'Invalid bet amount'}), 400
        
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT coins FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'User not found'}), 404
        coins = result[0]
        if coins < betAmount:
            return jsonify({'error': 'Insufficient coins'}), 400
        
        # Deduct bet amount from user's coins
        new_balance = coins - betAmount
        cursor.execute("UPDATE users SET coins = %s WHERE email = %s", (new_balance, email))
        # Insert bet details into the bets table
        print(f"Attempting to insert bet with email: {email}, eventId: {eventId}, selectedBetOption: {selectedBetOption}, betAmount: {betAmount}")
        cursor.execute("INSERT INTO bets (user_email, game_id, bet_details, bet_amount) VALUES (%s, %s, %s, %s)", (email,eventId,selectedBetOption,betAmount))
        db.commit()
        return jsonify({'message': 'Bet placed successfully'}), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid bet amount format'}), 400
    except Error as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
