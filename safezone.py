from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio credentials from .env file
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('sos.html')  # Make sure the sos.html is in the templates folder

@app.route('/safezone')
def safe():
    return render_template('safezone.html')

@app.route('/send-sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is missing"}), 400

    try:
        # Send SMS using Twilio
        message = client.messages.create(
            body=f"🚨 SOS Alert! Location: {message}",
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        return jsonify({"message": "SOS Alert Sent!", "sid": message.sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/index")
def index_page():
    return render_template("TRY.html")

@app.route('/location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        message_body = f"I'm at {latitude}, {longitude}. Stay Safe!"

        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )

        return jsonify({'message': 'Location shared successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error sending location!'}), 500

@app.route('/sound')
def sound():
    return render_template("index.html")

@app.route('/stop-sound', methods=['POST'])
def stop_sound():
    try:
        # Placeholder logic for stopping the sound
        # You may need to integrate server-side sound handling if necessary
        print("Sound stopped.")
        return jsonify({"message": "Sound stopped!"}), 200
    except Exception as e:
        print(f"Error stopping sound: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
