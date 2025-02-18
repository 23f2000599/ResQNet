from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/forgotpass')
def forgotpass():
    return render_template('forgotpass.html')
@app.route('/reset')
def reset():
    return render_template('reset.html')
@app.route('/home')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)