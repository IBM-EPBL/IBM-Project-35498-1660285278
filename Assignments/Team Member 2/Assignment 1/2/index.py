from flask import Flask, render_template, request, redirect, url_for, abort
app = Flask(__name__)
@app.route("/")
def output():
    return render_template("/index.html")
@app.route("/index", methods=["POST","GET"])
def index():
    if (request.method == "POST"):
        user = request.form.get("user")
        if (user == "admin"):
            return redirect(url_for("admin"))
        elif (user == "end"):
            abort(503)
        mail = request.form.get("mail")
        number = request.form.get("number")
        return render_template("/output.html", user=user, mail=mail, number=number)
@app.route("/admin")
def admin():
    return render_template("/admin.html")
if __name__ == "__main__":
    app.run(debug = True)