import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        auth_plugin='mysql_native_password',
    )

    mycursor = db.cursor()

    # Check if the 'users' database exists
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()
    database_exists = False
    for database in databases:
        if database[0] == 'users':
            database_exists = True
            break

    if database_exists:
        mycursor.execute("DROP DATABASE users")
        print("Existing database 'users' dropped.")

    # Create the 'users' database
    mycursor.execute("CREATE DATABASE users")
    print("Database 'users' created successfully.")

    # Select the 'users' database
    mycursor.execute("USE users")

    # Create the 'users' table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            bets JSON,
            coins INT NOT NULL DEFAULT 1000
        )
    """)
    print("Table 'users' created successfully.")

    # Create the 'bets' table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS bets (
            user_email VARCHAR(255) NOT NULL,
            game_id VARCHAR(255) NOT NULL,
            sports_key VARCHAR(255) NOT NULL,
            bet_details VARCHAR(255) NOT NULL,
            bet_amount INT NOT NULL,
            expected_winnings INT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
        """)
    print("Table 'bets' created successfully.")

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if db.is_connected():
        mycursor.close()
        db.close()
        print("MySQL connection is closed.")
