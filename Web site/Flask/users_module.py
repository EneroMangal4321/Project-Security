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
        sql = "SELECT username, salt, password FROM admin WHERE username = %s"
        sql_param = input_username
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchone()

        #Assign correct vars to sql result.
        username = result[0]
        salt = result[1]
        password = result[2]

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
