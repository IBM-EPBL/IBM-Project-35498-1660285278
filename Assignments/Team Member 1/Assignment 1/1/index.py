from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def output():
    return render_template("/index.html")
@app.route("/index", methods=["POST","GET"])
def index():
    if (request.method == "POST"):
        user = request.form.get("user")
        mail = request.form.get("mail")
        number = request.form.get("number")
        return render_template("/output.html", user=user, mail=mail, number=number)
if __name__ == "__main__":
    app.run(debug = True)