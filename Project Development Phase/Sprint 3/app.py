import os
import ibm_db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=txz44264;PWD=0e7ZwhLpS1dJFh9f","","")
print(conn)
@app.route("/")
def home():
    return render_template("/homepage.html")
@app.route("/signup.html")
def signup():
    return render_template("/signup.html")
@app.route("/signin.html")
def signin():
    return render_template("/signin.html")
@app.route("/user", methods=["POST", "GET"])
def user():
    if (request.method == "POST"):
        sem = request.form.get("sem")
        spw = request.form.get("spw")
        em_lst = []
        pw_lst = []
        try:
            data = ibm_db.exec_immediate(conn, "SELECT \"EMAIL\", \"PASSWORD\" FROM \"TXZ44264\".\"SIGNUPUSERDETAILS\";")
            while ibm_db.fetch_row(data) != False:
                em_lst.append(ibm_db.result(data, 0).replace(" ", ""))
                pw_lst.append(ibm_db.result(data, 1).replace(" ", ""))
            if (sem in em_lst and spw in pw_lst):
                return render_template("/user.html")
            else:
                return redirect("/signin.html")
        except Exception as e:
            print(e)
            return render_template("/error.html")
@app.route("/app", methods=["POST", "GET"])
def welcome():
    if (request.method == "POST"):
        fn = request.form.get("fn")
        ln = request.form.get("ln")
        em = request.form.get("em")
        pw = request.form.get("pw")
        cpw = request.form.get("cpw")
        message = Mail(
            from_email = "312819104004@act.edu.in",
            to_emails = em,
            subject = "Job Recommender - Account created successfully",
            html_content = '<p>You can now sign in with your credentials,<br>email: {}<br>password: {}</p>'.format(em, pw)
        )
        try:
            insert = ibm_db.exec_immediate(conn, "INSERT INTO \"TXZ44264\".\"SIGNUPUSERDETAILS\" VALUES ('{}', '{}', '{}', '{}');".format(fn, ln, em, pw))
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return render_template("/welcome.html", fn=fn, ln=ln, em=em, pw=pw, cpw=cpw)
        except Exception as e:
            print(e)
            return render_template("/error.html", fn=fn, ln=ln, em=em, pw=pw, cpw=cpw)
if __name__ == "__main__":
    app.run(debug = True)
