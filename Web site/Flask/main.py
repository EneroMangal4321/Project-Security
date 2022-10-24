#These modules will need to be imported, the modules starting with a dot are local modules.
import imp
import time
from flask import Flask, url_for, request, redirect, render_template, session, flash
from flask_wtf import FlaskForm, RecaptchaField
import mysql.connector as mysql
import secrets
import os
from users_module import *
#from audit_module import *

app = Flask(__name__)
#Keeps client-side sessions secure
app.secret_key = secrets.token_bytes(16)

#recaptcha keys
RECAPTCHA_PUBLIC_KEY = os.environ.get('6LcjBUgiAAAAABD2jof2yYBDNYNB1xGaslw0Q6iR')
RECAPTCHA_PRIVATE_KEY = os.environ.get('6LcjBUgiAAAAAKEpu9Qyut40w4wLdhgcvMyh_rpc')

#If users enter 'https://localhost:443' they wil be rerouted to the right url, based on a session cookie.
@app.route("/")
def welcome():
    if 'username' in session:
        return redirect(url_for("portal"))
    else:
        return redirect(url_for("login"))

#This route handles the signup proces. For this it uses functions from the user_module.
# When a post request is sent (by clicking the button) this function will take the entered data,
# and handle it accordingly. 
@app.route("/aanmelden", methods=["POST", "GET"])
def aanmelden():
    if 'username' in session:
        return redirect(url_for('welcome'))
    else:
        if request.method == "POST":

            username = request.form["gebruikersnaam"]
            password = request.form["wachtwoord"]
            password_repeat = request.form["wachtwoord-herhaling"]
            #if passwords match continue with data insertion.
            if password == password_repeat:
                status = sign_user_up(username, password)

                #User was succesfully added. 
                if status == 0:
                    flash("Gebruiker gemaakt, log nu in")
                    #audit(username, 0)
                    return redirect(url_for("login"))
                #Username was taken.    
                elif status == 1:
                    flash("gebruikersnaam niet beschikbaar")
                    #audit(username, 1)
                    return render_template('signup.html')

            #if passwords don't match let user try again.
            else:
                flash("De wachtwoorden komen niet overeen, probeer het opnieuw")
                #audit(username, 1)
                return render_template('signup.html')
                
        else:
            return render_template("signup.html")

#This route handles the login process. For this it uses functions from the user_module. 
# When a post request is sent (by clicking the button) this function will take the entered data,
# and handle it accordingly. Just like the sign-up route
@app.route("/login", methods=["POST", "GET"])
def login():
    #check if user is signed in
    if 'username' in session:
        return redirect(url_for('portal'))

    #if user is not signed in let them log in    
    else:
        if request.method == "POST":
            input_username = request.form["username"]
            input_username = [input_username]
            input_passwd = request.form["passwd"]
            status = user_login(input_username, input_passwd)
            # User logged in
            if status == 0:
                session['username'] = input_username[0]
                #audit(input_username[0], 2)
                return redirect(url_for("verify"))

            # Unsuccesfull log in attempts  
            elif status == 1:
                flash("gebruikersnaam en/of wachtwoord incorrect")
                #audit(input_username[0], 3)
                return render_template("login.html")
            elif status == 2:
                flash("gebruikersnaam en/of wachtwoord incorrect")
                #audit(input_username[0], 3)
                return render_template("login.html")

        #display page if not a post request
        else:
            return render_template("login.html")

@app.route("/verify", methods=["POST", "GET"])
def validate_verify():
    if request.method == "POST":
        input_code = request.form["verify_code"]
        input_code = int(input_code)
        status = check_verify(input_code)

        if status == 0:
            return redirect(url_for("portal"))
        else:
            return render_template("verify.html")
    return render_template("verify.html")


#This route lets user sign out. It does not do anything special, but just pops the username from the session.    
@app.route("/uitloggen")
def uitloggen():
    #check if user is logged in
    if 'username' in session:
        #delete user from session aka log them out
        session.pop('username', None)
        return redirect(url_for('login'))

    #if user not signed in tell them and make them login first
    else:
        flash("Om deze pagina te bezoeken moet u ingelogd zijn")
        return redirect(url_for("login"))

#This route shows all available portals and displays if users have captured flags for them.
# It does this with a special database user.
@app.route("/portal")
def portal():
    if 'username' in session:
        username = session["username"]
        return render_template("portal.html")

    else:
        flash("Om deze pagina te bezoeken moet u ingelogd zijn")
        return redirect(url_for("login"))

#This route shows our terms and conditions.
@app.route("/terms-and-conditions")
def terms():
    return render_template("t&c.html")
     
if __name__ == "__main__":
    app.run()