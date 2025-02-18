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

# Twilio credentials from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
recipient_phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")
# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Route to serve the HTML file
@app.route('/sos')
def index():
    return render_template('sos.html')  # Make sure the sos.html is in the templates folder

@app.route('/safezone')
def safe():
    return render_template('safezone.html')

from flask import jsonify, request
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os

# Validate phone number function
def validate_phone_number(phone_number):
    """Clean and validate phone number format."""
    # Remove any spaces, dashes, or parentheses
    cleaned_number = ''.join(filter(str.isdigit, phone_number))
    
    # Add country code if not present
    if not phone_number.startswith('+'):
        if cleaned_number.startswith('91'):
            cleaned_number = '+' + cleaned_number
        else:
            cleaned_number = '+91' + cleaned_number
            
    return cleaned_number

@app.route('/send-sos', methods=['POST'])
def send_sos():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message is missing"}), 400

        # Validate environment variables
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
            return jsonify({"error": "Twilio configuration is incomplete"}), 500

        # Validate and format phone numbers
        try:
            validated_recipient = validate_phone_number(RECIPIENT_PHONE_NUMBER)
            validated_twilio = validate_phone_number(TWILIO_PHONE_NUMBER)
            
            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Send SMS using Twilio
            message = client.messages.create(
                body=f"🚨 SOS Alert! Location: {message}",
                from_=validated_twilio,
                to=validated_recipient
            )
            
            print(f"SOS message sent successfully. SID: {message.sid}")
            return jsonify({
                "message": "SOS Alert Sent!", 
                "sid": message.sid
            }), 200

        except TwilioRestException as twilio_error:
            print(f"Twilio Error: {str(twilio_error)}")
            return jsonify({
                "error": "Failed to send SOS alert via Twilio",
                "details": str(twilio_error)
            }), 500

    except Exception as e:
        print(f"General Error in send_sos: {str(e)}")
        return jsonify({
            "error": "Error sending SOS alert",
            "details": str(e)
        }), 500


@app.route("/index")
def index_page():
    return render_template("TRY.html")


from flask import jsonify, request
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def validate_phone_number(phone_number):
    """Clean and validate phone number format."""
    # Remove any spaces, dashes, or parentheses
    cleaned_number = ''.join(filter(str.isdigit, phone_number))
    
    # Add country code if not present
    if not phone_number.startswith('+'):
        if cleaned_number.startswith('91'):
            cleaned_number = '+' + cleaned_number
        else:
            cleaned_number = '+91' + cleaned_number
            
    return cleaned_number

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

        # Validate environment variables
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
            return jsonify({
                "error": "Twilio configuration is incomplete",
                "details": "Missing required environment variables"
            }), 500

        try:
            # Validate phone numbers
            validated_recipient = validate_phone_number(RECIPIENT_PHONE_NUMBER)
            validated_twilio = validate_phone_number(TWILIO_PHONE_NUMBER)

            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Create message body
            message_body = f"📍 Location Alert!\nLatitude: {latitude}\nLongitude: {longitude}\nGoogle Maps: https://www.google.com/maps?q={latitude},{longitude}"

            # Send message
            message = client.messages.create(
                body=message_body,
                from_=validated_twilio,
                to=validated_recipient
            )

            print(f"Location message sent successfully. SID: {message.sid}")
            return jsonify({
                "message": "Location shared successfully!",
                "sid": message.sid
            }), 200

        except TwilioRestException as twilio_error:
            print(f"Twilio Error: {str(twilio_error)}")
            return jsonify({
                "error": "Failed to send location via Twilio",
                "details": str(twilio_error)
            }), 500

    except Exception as e:
        print(f"General Error in send_location: {str(e)}")
        return jsonify({
            "error": "Error processing location request",
            "details": str(e)
        }), 500


@app.route('/sound')
def sound():
    return render_template("index.html")

@app.route('/stop', methods=['GET'])  # Allow GET method here
def stop_sound():
    return render_template("stop.html")


if __name__ == '__main__':
    app.run(debug=True)
