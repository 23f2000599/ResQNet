from flask import Flask,render_template
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("marketpage.html")
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
if __name__=="__main__":
    app.run(debug=True)