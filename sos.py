#smriti's part
#SOS
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

if __name__ == '__main__':
    app.run(debug=True)
