from flask import Flask,render_template
app=Flask(__name__)
@app.route("/profile")
def index():
    return render_template("profile.html")

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/emergencycon")
def emergencycon():
    return render_template("emergencycon.html")

@app.route("/market")
def market():
    return render_template("market.html")

@app.route("/medical")
def medical():
    return render_template("medical.html")

if __name__=="__main__":
    app.run(debug=True)

