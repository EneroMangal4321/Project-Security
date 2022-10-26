#These modules will need to be imported, the modules starting with a dot are local modules.
import imp
import time
from flask import Flask, url_for, request, redirect, render_template, session, flash
from flask_wtf import FlaskForm, RecaptchaField
import mysql.connector as mysql
import secrets
import os
import socket
import mysql.connector
import functools
from users_module import *
#from audit_module import *

app = Flask(__name__)
#Keeps client-side sessions secure
app.secret_key = secrets.token_bytes(16)

# Connect to ban-database
banneddb = mysql.connect(host="localhost", port="3306", user="login", password="2Sasf@csAas3", database="psdb")

bannedcursor = banneddb.cursor(buffered=True)

# Get client IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print("Your IP is: " + ip_address)

#recaptcha keys
RECAPTCHA_PUBLIC_KEY = os.environ.get('6LcjBUgiAAAAABD2jof2yYBDNYNB1xGaslw0Q6iR')
RECAPTCHA_PRIVATE_KEY = os.environ.get('6LcjBUgiAAAAAKEpu9Qyut40w4wLdhgcvMyh_rpc')

@app.route("/")
def autoblock():
    # Pre client IP register check
    bannedcursor.execute("SELECT ip_address FROM banned_table")

    ip_list = bannedcursor.fetchall()

    for i in ip_list:
        a = str(i)
        ip_list =a.split(",")[0]
        print(ip_list)

    if 'username' in session:
        return redirect(url_for("portal"))
    # If ip_address in ip_list, -> count post requests + 1 -> if count = 5, -> change banned variable to 1 -> if banned variable =1 
    # -> return render template denied -> if banned variable =1 change banned variable after 5 mins back to 0 -> 
    # if banned variable =0 && login =correct, login
    if ip_address in ip_list:
        print("Ip exists in banlist")
        # Check count, if < 5, add 1, if = 5, ban
        countquery = "SELECT login_count FROM banned_table WHERE (ip_address = (%s))"
        bannedcursor.execute(countquery,(ip_address, ))
        currentlogin_count = functools.reduce(lambda sub, ele: sub * 10 + ele, bannedcursor.fetchone())
        print(currentlogin_count)
        maxlogin_count = 5
        newlogin_count = currentlogin_count + 1
        print(newlogin_count)
        checkbanquery = "SELECT banned FROM banned_table WHERE (ip_address = (%s))"
        bannedcursor.execute(checkbanquery,(ip_address, ))
        checkban_count = functools.reduce(lambda sub, ele: sub * 10 + ele, bannedcursor.fetchone())
        print(checkban_count)
        if currentlogin_count < maxlogin_count:
            addcountquery = "UPDATE banned_table SET login_count =(%s) WHERE ip_address=(%s)"
            bannedcursor.execute(addcountquery,(newlogin_count, ip_address, ))
            banneddb.commit()
            print(newlogin_count)
            return render_template('login.html')
        if currentlogin_count == maxlogin_count:
            newban_count = 1
            banquery = "UPDATE banned_table SET banned=(%s) WHERE ip_address=(%s)"
            bannedcursor.execute(banquery,(newban_count, ip_address, ))
            banneddb.commit()
        if checkban_count == 1:
            return render_template('denied.html')
      
    else:
        # Registers client IP to database
        insertquery = "INSERT INTO banned_table (ip_address, banned, login_count) VALUES (%s, %s, %s)"
        bannedcursor.execute(insertquery,(ip_address, 0, 0, ))
        banneddb.commit()
        print("Ip Inserted")
        return redirect(url_for("login"))

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
                return redirect(url_for("portal"))

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
