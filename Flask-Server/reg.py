import mysql.connector
from mysql.connector import Error
import re
import dns.resolver
import socket
import smtplib
import bcrypt


def valid_email(email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return re.fullmatch(email_regex, email) is not None

def valid_password(password, passwordRedo):
    password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    if re.fullmatch(password_regex, password) is not None:
        if password == passwordRedo:
            return True
        else:
            print("Passwords do not match")
            return False
    else:
        print("Password does not follow the guidelines")
        return False

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

        if code == 250:
            return True
        else:
            print('Please enter a valid email address')
    except dns.resolver.NoAnswer:
        print(f"No MX records found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"Domain '{domain}' does not exist")
    except Exception as e:
        print(f"Error: {e}")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        auth_plugin='mysql_native_password',
        database="users"
    )

    if db.is_connected():
        print("Successfully connected to the database")

    while True:
        email_input = input("Please enter your email address: ")
        if valid_email(email_input):
            if domain_validator(email_input):
                break

    while True:
        passwordInp1 = input("Please enter your password: ")
        passwordInp2 = input("Please re-enter your password: ")
        if valid_password(passwordInp1, passwordInp2):
            passwordInp1 = bcrypt.hashpw(passwordInp1.encode('utf-8'), bcrypt.gensalt())
            break

    mycursor = db.cursor()

    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        coins INT NOT NULL
    )
    """)

    check_email_query = "SELECT id FROM users WHERE email = %s"
    mycursor.execute(check_email_query, (email_input,))
    result = mycursor.fetchone()

    if result:
        print("Email address already exists in the database.")
    else:
        sql_insert_query = """
        INSERT INTO users (name, email, password, coins)
        VALUES (%s, %s, %s, %s)
        """
        name_input = input("Please enter your name: ")
        coins_input = 1000

        insert_values = (name_input, email_input, passwordInp1, coins_input)
        mycursor.execute(sql_insert_query, insert_values)

        db.commit()
        print(insert_values)

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if db.is_connected():
        mycursor.close()
        db.close()
        print("MySQL connection is closed")

