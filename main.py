from flask import Flask,render_template
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("marketpage.html")
@app.route("/emergencefood")
def emergencefood():
    return render_template("emergencefood.html")


if __name__=="__main__":
    app.run(debug=True)