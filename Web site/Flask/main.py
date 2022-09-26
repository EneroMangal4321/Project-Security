#!/usr/bin/env python

import hashlib
import random
from flask import Flask, url_for, request, redirect, render_template, session, flash
import mysql.connector as mysql




app = Flask(__name__)
app.secret_key = "ABC"

db = mysql.connect(
        host = "localhost",
        user = "login",      
        passwd = "2Sasf@csAas3",    
        database = "psdb")


#########################################################################################################################
#                                                                                                                       #
# The part below this are the fuctions that are used across the website                                                 #
#                                                                                                                       #
#########################################################################################################################


# function to see if the user that has been filled in already exists
def user_exists(username):
    # open db session
    cursor = db.cursor()
    # see if the user exists in the database
    cursor.execute(f"SELECT username FROM User WHERE username = '%s'" % (username))
    # fetch the result of the above query
    fetchresult = cursor.fetchmany()
    # close db session
    # if fetchresult[0][0] == username:
    #     return True
    # else:
    #     return False
    if fetchresult is not None:
        for row in fetchresult:
            if row[0] == username:
                return True
            else:
                return False
    else:
        return False


    # close db session
    cursor.close()

# function to see if the email that has been filled in already exists  
def email_exists(email):
    # open db session
    cursor = db.cursor()
    # make the email into a variable
    # email = request.form[f'Lusername']
    cursor.execute(f"SELECT email FROM User WHERE email = '%s'" % (email))
    # fetch the result of the above query
    fetchresult = cursor.fetchmany()
    # Checks if 
    if fetchresult is not None:
        for row in fetchresult:
            if row[0] == email:
                return True
            else:
                return False
    else:
        return False

    # if fetchresult[0][0] == email:
    #     return True
    # else:
    #     return False
    # # close db session
    cursor.close()
    
# function to make a salt
def make_salt():
    # makes a random 32 byte number that will be used as salt
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(32):
        chars.append(random.choice(ALPHABET))

    salt = "".join(chars)
    return salt

# checks if salt 
def salt_check(salt):
    # open db session
    cursor = db.cursor()
    # see if the salt is already in the db
    cursor.execute(f"SELECT salt FROM User WHERE salt = '%s'" % (salt))
    fetchresult = cursor.fetchone()
    # checks if salt is in db
    if fetchresult is not None:
        for row in fetchresult:
            if row[0] == salt:
                return True
            else:
                return False
    else:
        return False
    # close db session
    cursor.close()
    
# function to encrypt the password given
def encrypt(password, salt):
    # encodes the password
    plaintext = str(password)+str(salt)
    # hashes the password with sha256 
    digest = hashlib.sha256(plaintext.encode())
    # changes the digest into a hex
    hex_Hash = digest.hexdigest()
    # returns the hex hash
    return hex_Hash

# function to add the user to the db
def add_new_user_to_database(username, email, encrypt_password, salt):
    # open db session
    cursor = db.cursor()
    # add user to DB
    cursor.execute(f"INSERT INTO User (username, email, password, salt) VALUES ('{username}','{email}', '{encrypt_password}', '{salt}');")
    # commit changes
    db.commit()
    # close db session
    cursor.close()


#########################################################################################################################
#                                                                                                                       #
# The part below this is for the Dutch end of the website                                                               #
#                                                                                                                       #
#########################################################################################################################

@app.route('/')
def indexNL():
    return render_template('index-NL.html')


@app.route('/login', methods=['GET', 'POST'])
def loginNL():
    cursor = db.cursor()
    mail_check = '@'
    if request.method == f'POST' :       
        # check if the username filled in is an email or not
        if mail_check in request.form[f'Lusername']:
            Lemail = request.form[f'Lusername']
            Lpassword = request.form[f'Lpassword']
            # checks if the email exists in the db
            if email_exists(Lemail) == True:
                # Get salt of the email in db
                cursor.execute(f"SELECT salt FROM User WHERE email = '%s'" % (Lemail))
                salt = cursor.fetchmany()
                # encrypt the password given with the salt from the db
                Lpassword = encrypt(Lpassword, salt[0])
                # get encrypted password from db
                cursor.execute(f"SELECT password FROM User WHERE email = '%s'" % (Lemail))
                encrpwd = cursor.fetchmany()

                # check if passwords are the same
                if Lpassword == encrpwd[0]:
                    # maakt een cookie aan met de username
                    session['username'] = request.form['Lemail']
                    flash(u"You have been logged in", 'info')
                    return redirect("/")
                else:
                    flash("de login gegevens kloppen niet", 'info')
                    return redirect('/login')
            else:
                flash("de login gegevens kloppen niet", 'info')
                return redirect('/login')
                
        
        else:
            Lusername = request.form[f'Lusername']
            Lpassword = request.form[f'Lpassword']
            # checks if the email exists in the db
            if user_exists(Lusername) == True:
                # Get salt of the email in db
                cursor.execute(f"SELECT salt FROM User WHERE username = '%s'" % (Lusername))
                salt = cursor.fetchmany()
                # encrypt the password given with the salt from the db
                Lpassword = encrypt(Lpassword, salt[0])
                # get encrypted password from db
                cursor.execute(f"SELECT password FROM User WHERE username =  '%s'" % (Lusername))
                encrpwd = cursor.fetchmany()
                # check if passwords are the same
                if Lpassword == encrpwd[0]:  
                    flash(u"You have been logged in")
                    # maakt een cookie aan met de username                    
                    session['username'] = request.form['Lusername']
                    return redirect("/")
                else:
                    flash("de login gegevens kloppen niet", 'info')
                    return redirect('/login')
            else:
                flash("de login gegevens kloppen niet", 'info')
                return redirect('/login')
    else:
        return render_template('Login-NL.html')               


@app.route('/aanmelden', methods=['GET', 'POST'])
def aanmelden():
    error = None;
    if request.method == f'POST':
        Susername = request.form[f'Susername']
        Semail = request.form[f'Semail']
        Spassword1 = request.form[f'Spassword1']
        Spassword2 = request.form[f'Spassword2']
     
        # check if username and email already exists
        if user_exists(Susername) == True and email_exists(Semail) == True:
            flash('De gebruikersnaam en email zijn al in gebruik', 'info')
            return redirect('/aanmelden')
        # check if username already exists
        elif user_exists(Susername) == True:
            flash('De gebruikersnaam is al in gebruik', 'info')
            return redirect('/aanmelden')
        # check if email already exists
        elif email_exists(Semail) == True:
            flash('De email adres is al in gebruik', 'info')
            return redirect('/aanmelden')
        # check if password is the same as second given password
        elif Spassword1 != Spassword2:
            flash("De wachtwoorden komen niet overeen", 'info')
            return redirect('/aanmelden')
        else:
            # make a salt for the new user
            salt = make_salt()
            #check if salt exists
            if salt_check(salt) == True:
                salt = make_salt()
            else:
                salt = salt



            # encrypt the password with the previously made salt
            Sencrypt_password = encrypt(Spassword1, salt)
            # adds the user to the database with username, email and the encrypted password
            add_new_user_to_database(Susername, Semail, Sencrypt_password, salt)
            flash(u'Gebruiker is aangemaakt')
            # maakt een cookie aan met de username      
            session['username'] = request.form['Susername']
            return redirect("/")
    else:
        return render_template('aanmelden.html') 


@app.route('/logout')
def logoutNL():
    # verwijdert de cookie
    session['username'] = None
    return redirect("/")



@app.route('/overons')
def overons():
    return render_template('Overons.html')


if __name__ == "__main__":
    app.run(debug=True)
