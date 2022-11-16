import re
import os
import ibm_db
from flask import flash
from flask import Flask
from flask import request
from flask import redirect
from bs4 import BeautifulSoup
from flask import render_template
from urllib.request import urlopen
from urllib.request import Request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=txz44264;PWD=0e7ZwhLpS1dJFh9f","","")

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
            f = open("./sendgrid.txt", "r")
            sg = SendGridAPIClient(f.read())
            response = sg.send(message)

            return render_template("/welcome.html")

        except Exception as e:

            print(e)

            return render_template("/error.html")

@app.route("/job", methods=["POST", "GET"])

def job():

    if (request.method == "POST"):

        search = request.form.get("search")
        link = "https://www.glassdoor.com/Job/india-{}-jobs-SRCH_IL.0,5_IN115_KO6,11.htm".format(search)

        return render_template("/job.html", link=link)

if __name__ == "__main__":
    app.run(debug = True)