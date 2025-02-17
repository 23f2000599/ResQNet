from flask import Flask,render_template
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("profile.html")

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/emergencycon")
def emergencycon():
    return render_template("emergencycon.html")

if __name__=="__main__":
    app.run(debug=True)

