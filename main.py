from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def validate():
    un = request.form['username']
    pw = request.form['password']
    vpw = request.form['verify']
    email = request.form['email']

    un_error = ""
    pw_error = ""
    vpw_error = ""
    email_error = ""

    if un == "":
        un_error = "Username not valid."
    elif " " in un:
        un_error= "Username cannot contain a space."
    elif len(un) < 3 or len(un) > 20:
        un_error = "Username not valid, must be 3-20 characters"

    if pw == "":
        pw_error = "Missing Password"
    elif " " in pw:
        pw_error= "Password cannot contain a space."
    elif len(pw) <3 or len(pw) > 20:
        pw_error = "Password not valid, must be 3-20 characters"
    
    if vpw == "":
        vpw_error = "Nothing entered"
    elif len(vpw) < 3 or len(vpw) > 20:
        vpw_error = "Passwords not valid and did not match"
    elif vpw != pw:
        vpw_error = "Passwords don't match"

    if email:
        if len(email) < 3 or len(email) > 20:
            email_error = "Email not valid, must be 3-20 characters"
        email_ver = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I)
        if not email_ver:
            email_error = "Email not valid"

    if un_error or pw_error or vpw_error or email_error:
        return render_template("index.html", username = un, email = email, username_error = un_error, password_error = pw_error,
        vpw_error = vpw_error, email_error = email_error )
    else:
        return redirect('/welcome?username={0}'.format(un))



@app.route("/welcome", methods = ['GET'])
def welcome():
    name = request.args.get("username")
    return render_template("welcome.html", name = name)

app.run()