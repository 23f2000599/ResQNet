from flask import Flask,render_template
app = Flask(__name__)
app.secret_key = 'lifesucks'
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app.secret_key = 'lifesucks'

# Set the database URI to use the 'instance' folder for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warnings

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Initialize the database
db = SQLAlchemy(app)

# Function to recreate the database
import os
import sqlite3

def initialize_db():
    db_path = os.path.join(app.instance_path, 'users.db')
    
    # Check if database file exists
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the user table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            full_name TEXT,
                            date_of_birth DATE,
                            phone_number TEXT,
                            address TEXT,
                            blood_type TEXT,
                            allergies TEXT,
                            emergency_contact_name TEXT,
                            emergency_contact_relation TEXT,
                            emergency_contact_phone TEXT
                        )''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    else:
        print("Database already exists")

# Replace recreate_db() call with initialize_db()
initialize_db()

@app.route('/file')
def file():
    return render_template('file.html')

def get_user_details(user_id):
    try:
        db_path = os.path.join(app.instance_path, 'users.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user details from database
        cursor.execute('''SELECT * FROM user WHERE id = ?''', (user_id,))
        user = cursor.fetchone()
        print(f"Fetched user details: {user}")  # Debug print
        
        if user:
            # Create dictionary with all user details
            user_details = {
                'username': user[1],
                'email': user[2],
                'full_name': user[4],
                'date_of_birth': user[5],
                'phone_number': user[6],
                'address': user[7],
                'blood_type': user[8],
                'allergies': user[9],
                'emergency_contact_name': user[10],
                'emergency_contact_relation': user[11],
                'emergency_contact_phone': user[12]
            }
            print(f"Returning user details: {user_details}")  # Debug print
            return user_details
        return None
        
    except Exception as e:
        print(f"Error in get_user_details: {str(e)}")  # Debug print
        return None
    finally:
        conn.close()


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/details')
def details():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_details = get_user_details(session['user_id'])
    if user_details:
        return render_template('details.html', **user_details)
    else:
        flash('User details not found', 'error')
        return redirect(url_for('login'))


from flask import jsonify, request

@app.route('/emergencycon')
def emergencycon():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    try:
        db_path = os.path.join(app.instance_path, 'users.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get emergency contact details of logged in user
        cursor.execute('''
            SELECT emergency_contact_name, emergency_contact_relation, emergency_contact_phone 
            FROM user 
            WHERE id = ?
        ''', (session['user_id'],))
        
        contact = cursor.fetchone()
        print(f"Emergency contact fetched: {contact}")  # Debug print
        
        if contact:
            contact_details = {
                'name': contact[0],  # emergency_contact_name
                'relation': contact[1],  # emergency_contact_relation
                'phone': contact[2]  # emergency_contact_phone
            }
            print(f"Contact details being sent to template: {contact_details}")  # Debug print
            return render_template('emergencycon.html', contact=contact_details)
        else:
            return render_template('emergencycon.html', contact=None)
            
    except Exception as e:
        print(f"Error fetching emergency contacts: {str(e)}")
        flash('An error occurred while fetching emergency contacts', 'error')
        return render_template('emergencycon.html', contact=None)
    finally:
        conn.close()

@app.route('/update_emergency_contact', methods=['POST'])
def update_emergency_contact():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug print
        
        db_path = os.path.join(app.instance_path, 'users.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update emergency contact details
        cursor.execute('''
            UPDATE user 
            SET emergency_contact_name = ?,
                emergency_contact_relation = ?,
                emergency_contact_phone = ?
            WHERE id = ?
        ''', (
            data['name'],
            data['relation'],
            data['phone'],
            session['user_id']
        ))
        
        conn.commit()
        print("Emergency contact updated successfully")  # Debug print
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error updating emergency contact: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/editprofile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    try:
        db_path = os.path.join(app.instance_path, 'users.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if request.method == 'POST':
            # Get form data
            updated_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'phone_number': request.form['phone_number'],
                'address': request.form['address'],
                'blood_type': request.form['blood_type'],
                'allergies': request.form['allergies'],
                'emergency_contact_name': request.form['emergency_contact_name'],
                'emergency_contact_relation': request.form['emergency_contact_relation'],
                'emergency_contact_phone': request.form['emergency_contact_phone']
            }
            
            print(f"Updating profile with data: {updated_data}")  # Debug print

            # Update user data in database
            cursor.execute('''
                UPDATE user 
                SET full_name = ?,
                    email = ?,
                    phone_number = ?,
                    address = ?,
                    blood_type = ?,
                    allergies = ?,
                    emergency_contact_name = ?,
                    emergency_contact_relation = ?,
                    emergency_contact_phone = ?
                WHERE id = ?
            ''', (
                updated_data['full_name'],
                updated_data['email'],
                updated_data['phone_number'],
                updated_data['address'],
                updated_data['blood_type'],
                updated_data['allergies'],
                updated_data['emergency_contact_name'],
                updated_data['emergency_contact_relation'],
                updated_data['emergency_contact_phone'],
                session['user_id']
            ))
            
            conn.commit()
            print("Profile updated successfully")  # Debug print
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('details'))
        
        else:
            # GET request - show current user data in form
            cursor.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],))
            user = cursor.fetchone()
            
            if user:
                user_details = {
                    'full_name': user[4],
                    'email': user[2],
                    'phone_number': user[6],
                    'address': user[7],
                    'blood_type': user[8],
                    'allergies': user[9],
                    'emergency_contact_name': user[10],
                    'emergency_contact_relation': user[11],
                    'emergency_contact_phone': user[12]
                }
                return render_template('editprofile.html', **user_details)
            else:
                flash('User not found', 'error')
                return redirect(url_for('login'))

    except Exception as e:
        print(f"Error in edit_profile: {str(e)}")  # Debug print
        flash('An error occurred while updating profile', 'error')
        return redirect(url_for('details'))
    finally:
        conn.close()

@app.route("/market")
def market():
    return render_template("market.html")

@app.route("/medical")
def medical():
    return render_template("medical.html")

@app.route('/marketpage')
def marketpage():
    print("Marketpage route accessed")  # Debugging
    return render_template('marketpage.html')

@app.route("/emergencefood")
def emergencefood():
    return render_template("emergencefood.html")
@app.route("/essentials")
def essentials():
    return render_template("essentials.html")
@app.route("/medicals")
def medicals():
    return render_template("medicals.html")
@app.route("/cart")
def cart():
    return render_template("cart.html")
from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()



# Email configuration from .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Route to serve the HTML file
@app.route('/sos')
def sos():
    return render_template('sos.html')  # Make sure the sos.html is in the templates folder

@app.route('/safezone')
def safe():
    return render_template('safezone.html')

def send_email_alert(subject, message_body):
    """Send email alert using Gmail SMTP."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message_body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False


@app.route('/send-sos', methods=['POST'])
def send_sos():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message is missing"}), 400

        # Send email alert
        if send_email_alert("🚨 SOS Alert - ResQNet", f"🚨 SOS Alert! Location: {message}"):
            return jsonify({"message": "SOS Alert Sent!"}), 200
        else:
            return jsonify({
                "error": "Failed to send SOS alert",
                "details": "Email service unavailable"
            }), 500

    except Exception as e:
        print(f"General Error in send_sos: {str(e)}")
        return jsonify({
            "error": "Error sending SOS alert",
            "details": str(e)
        }), 500







@app.route('/location', methods=['POST'])
def send_location():
    try:
        # Get location data
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Validate location data
        if not all([latitude, longitude]):
            return jsonify({
                "error": "Missing location data",
                "details": "Both latitude and longitude are required"
            }), 400

        # Create message body
        message_body = f"📍 Location Alert!\nLatitude: {latitude}\nLongitude: {longitude}\nGoogle Maps: https://www.google.com/maps?q={latitude},{longitude}"
        
        # Send email alert
        if send_email_alert("📍 Location Alert - ResQNet", message_body):
            return jsonify({"message": "Location shared successfully!"}), 200
        else:
            return jsonify({
                "error": "Failed to send location alert",
                "details": "Email service unavailable"
            }), 500

    except Exception as e:
        print(f"General Error in send_location: {str(e)}")
        return jsonify({
            "error": "Error processing location request",
            "details": str(e)
        }), 500


# @app.route('/sound')
# def sound():
#     return render_template("index.html")

@app.route('/stop', methods=['GET'])  # Allow GET method here
def stop_sound():
    return render_template("stop.html")


@app.route('/')
def index():
    return render_template('index.html')

from flask import session, flash, redirect, url_for  # Add these imports at the top

from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for

from werkzeug.security import check_password_hash
from flask import flash, redirect, url_for, render_template
import sqlite3
import os

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt - Username: {username}, Password: {password}")  # Debug prin
        try:
            db_path = os.path.join(app.instance_path, 'users.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            
            print(f"Database query result - User: {user}")  # Debug print
            
            if user:
                # User found with matching username and password
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user[0]
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            flash('An error occurred', 'error')
            return render_template('login.html')
        finally:
            conn.close()

    return render_template('login.html')


from flask import request, flash, redirect, url_for

from werkzeug.security import generate_password_hash
import sqlite3


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("Signup form submitted")  # Debug print
        
        # Get form data
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        address = request.form['address']
        blood_type = request.form['blood_type']
        allergies = request.form['allergies']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_relation = request.form['emergency_contact_relation']
        emergency_contact_phone = request.form['emergency_contact_phone']

        try:
            db_path = os.path.join(app.instance_path, 'users.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Insert user data
            cursor.execute('''
                INSERT INTO user (email, username, password, full_name, date_of_birth, 
                phone_number, address, blood_type, allergies, emergency_contact_name, 
                emergency_contact_relation, emergency_contact_phone) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, username, password, full_name, date_of_birth, phone_number, 
                 address, blood_type, allergies, emergency_contact_name, 
                 emergency_contact_relation, emergency_contact_phone))
            
            conn.commit()
            print("User data inserted successfully")  # Debug print

            # Set session variables
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = cursor.lastrowid

            flash('Registration successful!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(f"Error in signup: {str(e)}")  # Debug print
            flash('An error occurred during registration', 'error')
            return render_template('signup.html')
        finally:
            conn.close()

    return render_template('signup.html')






@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        print(f"Form data received - Email: {email}, New password: {new_password}, Confirm password: {confirm_password}")

        if new_password != confirm_password:
            print("Passwords don't match!")
            flash('Passwords do not match', 'error')
            return redirect(url_for('forgotpass'))

        try:
            db_path = os.path.join(app.instance_path, 'users.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check current data in the table
            print("Current data in user table:")
            cursor.execute('SELECT * FROM user')
            all_users = cursor.fetchall()
            print(all_users)

            # Check if email exists
            cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
            user = cursor.fetchone()
            print(f"Found user: {user}")

            if user:
                # Update password
                cursor.execute('UPDATE user SET password = ? WHERE email = ?', (new_password, email))
                conn.commit()
                
                # Verify the update
                cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
                updated_user = cursor.fetchone()
                print(f"After update - User data: {updated_user}")
                
                flash('Password updated successfully!', 'success')
                return redirect(url_for('login'))
            else:
                print(f"No user found with email: {email}")
                flash('Email address not found', 'error')
                return redirect(url_for('forgotpass'))

        except Exception as e:
            print(f"Error updating password: {str(e)}")
            flash('An error occurred', 'error')
            return redirect(url_for('forgotpass'))
        finally:
            conn.close()

    return render_template('forgotpass.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')
@app.route('/home')
def home():
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True,port=8000)

