from flask import Flask, url_for, request, render_template, redirect
import mysql.connector as mysql
import secrets
import hashlib
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import random

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

sender_email = "verify.sec.2022@outlook.com"
password_email = "Verify.Sec"

#A function that checks users creds. It takes a username and a password, and will return a status.
# status = 0 means password and username match, status = 1 means username and/or password do not 
# match and status = 2 means invalid username.
def user_login(input_username, input_passwd):
    try:
        #Establish DB connection with login user.
        db = mysql.connect(
        host = "localhost",
        user = "login",
        passwd = "2Sasf@csAas3",
        database = "psdb")

        #A prepared statement to get username, salt and hashed password from db.
        mycursor = db.cursor()
        sql = "SELECT username, salt, password, email FROM admin WHERE username = %s"
        sql_param = input_username
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchone()

        #Assign correct vars to sql result.
        username = result[0]
        salt = result[1]
        password = result[2]
        reciever_email = result[3]

        #Revert username to correct format.
        input_username = input_username[0]
        
        #Hash the password entered by user.
        #input_passwd = input_passwd + salt
        #input_passwd = hashlib.sha256(input_passwd.encode('utf-8')).hexdigest()

        mycursor.close()
        db.close()

        #check if username and passwords match
        if input_username == username and input_passwd == password:
            status = 0

            try:
                rando_nr = random.randint(1000,9999)
                msg = EmailMessage()
                msg["Subject"] = "Verificatie Code"
                msg["From"] = formataddr(("Verificatie Code", f"{sender_email}"))
                msg["To"] = reciever_email
                msg["BCC"] = sender_email

                msg.set_content(
                    f"""Beste 'Naam hier',\n
                    Uw verificatie nummer is {rando_nr} gebruik dit nummer om de 2 stap verificatie af te ronden."""
                )

                with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
                    server.starttls()
                    server.login(sender_email, password_email)
                    server.sendmail(sender_email, reciever_email, msg.as_string())
                
                #code die verificatiecode in db zet
                mycursor = db.cursor()
                sql = f"UPDATE Users SET verificatie = %s WHERE username = %s;"
                sql_param = [rando_nr, username]
                mycursor.execute(sql, sql_param)
                result = mycursor.fetchall()

            except:
                return status
            return status

        #if username and password dont match display error message 
        else:
            status = 1
            return status

    #if username doesn't exist an error message will be displayed
    except TypeError:

            status = 2
            return status

def check_verify(input_code):
    try: 
        db = mysql.connect(
        host = "localhost",
        user = "login",
        passwd = "2Sasf@csAas3",
        database = "psdb")

        mycursor = db.cursor()
        sql = "SELECT verificatie FROM admin WHERE id = %s"
        sql_param = 1
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchone()

        verify_code = result[0]
        verify_code1 = result

        print(verify_code)
        print(verify_code1)

        if input_code == verify_code:
            status = 0
            return status

    except:
        status = 1
        return status