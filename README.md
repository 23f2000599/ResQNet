# ResQNet - Emergency Response System

A comprehensive emergency response web application built with Flask that provides SOS alerts, location sharing, user management, and emergency marketplace functionality.

## Features

### 🚨 Emergency Services
- **SOS Alert System**: Send emergency alerts via email
- **Location Sharing**: Share GPS coordinates with emergency contacts
- **Emergency Contact Management**: Store and manage emergency contact information

### 👤 User Management
- User registration and authentication
- Profile management with medical information
- Password recovery system
- Session management

### 🛒 Emergency Marketplace
- Emergency food supplies
- Medical essentials
- Safety equipment
- Shopping cart functionality

### 📱 Additional Features
- Responsive web design
- Real-time location tracking
- Email notification system
- SQLite database integration

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ResQNet
```

2. **Install dependencies**
```bash
pip install flask flask-sqlalchemy python-dotenv
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=emergency_contact@example.com
```

4. **Run the application**
```bash
python main.py
```

The application will be available at `http://127.0.0.1:5000`

## Configuration

### Email Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for the application
3. Update the `.env` file with your credentials

### Database
The application uses SQLite database stored in the `instance/users.db` file. The database is automatically initialized on first run.

## Usage

### Getting Started
1. Visit the homepage at `http://127.0.0.1:5000`
2. Register a new account or login with existing credentials
3. Complete your profile with emergency contact information

### Emergency Features
- **SOS Alert**: Click the SOS button to send emergency alerts
- **Location Sharing**: Share your current location with emergency contacts
- **Emergency Contacts**: Manage your emergency contact information

### Marketplace
- Browse emergency supplies in different categories
- Add items to cart
- Manage your shopping cart

## Project Structure

```
ResQNet/
├── main.py                 # Main Flask application
├── .env                    # Environment variables
├── screenshots/            # Page screenshots
├── templates/              # HTML templates
│   ├── index.html         # Homepage
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── home.html          # User dashboard
│   ├── sos.html           # SOS alert page
│   ├── market.html        # Marketplace
│   └── ...                # Other templates
├── static/                 # CSS, JS, images
└── instance/
    └── users.db           # SQLite database
```

## API Endpoints

### Authentication
- `GET /` - Homepage
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /signup` - Registration page
- `POST /signup` - Process registration
- `GET /forgotpass` - Password recovery

### Emergency Services
- `GET /sos` - SOS alert page
- `POST /send-sos` - Send SOS alert
- `POST /location` - Share location

### User Management
- `GET /home` - User dashboard
- `GET /details` - User profile
- `GET /editprofile` - Edit profile
- `POST /editprofile` - Update profile
- `GET /emergencycon` - Emergency contacts
- `POST /update_emergency_contact` - Update emergency contact

### Marketplace
- `GET /market` - Main marketplace
- `GET /marketpage` - Product listings
- `GET /emergencyfood` - Food supplies
- `GET /essentials` - Essential items
- `GET /medicals` - Medical supplies
- `GET /cart` - Shopping cart

## Database Schema

### User Table
- `id` - Primary key
- `email` - User email
- `username` - Username
- `password` - Password (plain text)
- `full_name` - Full name
- `date_of_birth` - Date of birth
- `phone_number` - Phone number
- `address` - Address
- `blood_type` - Blood type
- `allergies` - Medical allergies
- `emergency_contact_name` - Emergency contact name
- `emergency_contact_relation` - Relationship
- `emergency_contact_phone` - Emergency contact phone

## Technologies Used

- **Backend**: Flask, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Email**: SMTP (Gmail)
- **Environment**: Python 3.x

## Security Notes

- Passwords are stored in plain text (consider implementing hashing)
- Session management using Flask sessions
- Email credentials stored in environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please contact the development team or create an issue in the repository.