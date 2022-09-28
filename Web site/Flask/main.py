#!/usr/bin/env python

import hashlib
import random
from flask import Flask, url_for, request, redirect, render_template, session, flash
import mysql.connector as mysql
from .users_module import *


app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

@app.route("/")
def indexNL():
    return render_template('index-NL.html')


@app.route("/login", methods=['GET', 'POST'])
def loginNL():
    #check if user is signed in
    if 'username' in session:
        return redirect(url_for('welcome'))

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
                audit(input_username[0], 2)
                return redirect(url_for("welcome"))

            # Unsuccesfull log in attempts  
            elif status == 1:
                flash("gebruikersnaam en/of wachtwoord incorrect")
                audit(input_username[0], 3)
                return render_template("login.html")
            elif status == 2:
                flash("gebruikersnaam en/of wachtwoord incorrect")
                audit(input_username[0], 3)
                return render_template("login.html")

        #display page if not a post request
        else:
            return render_template('Login-NL.html')               


@app.route("/logout")
def logoutNL():
    #check if user is logged in
    if 'username' in session:
        #delete user from session aka log them out
        session.pop('username', None)
        return redirect(url_for('loginNL'))

    #if user not signed in tell them and make them login first
    else:
        flash("Om deze pagina te bezoeken moet u ingelogd zijn")
        return redirect(url_for("loginNL"))


@app.route("/overons")
def overons():
    return render_template('Overons.html')


if __name__ == "__main__":
    app.run(debug=True)