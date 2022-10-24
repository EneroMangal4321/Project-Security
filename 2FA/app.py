from flask import Flask, url_for, request, render_template, redirect
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import random
import mysql.connector as mysql

app = Flask(__name__)

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

sender_email = "verify.sec.2022@outlook.com"
password_email = "Verify.Sec"

@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        # try:
        reciever = request.form["email"]
        rando_nr = send_email(reciever)

        #Establish DB connection with flag user
        db = mysql.connect(
        host = "database",
        # host = "localhost",
        user = "flag",
        passwd = "8iAnDu#@a4%ac",
        database = "paddb")

        #code die id en email uit db haalt door middel van gebruikersnaam
        mycursor = db.cursor()
        sql = f"SELECT id, email from Users WHERE user_username = %s;"
        sql_param = [username]
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchall()
        
        #code die verificatie email stuurt naar email
        rando_nr = send_email(reciever)


        #code die verificatiecode in db zet
        mycursor = db.cursor()
        sql = f"UPDATE Users SET code = %s WHERE id = %s;"
        sql_param = [rando_nr, id]
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchall()

        #code die opgegeven code vergelijkt met code uit db
        mycursor = db.cursor()
        sql = f"SELECT code from Users WHERE id = %s;"
        sql_param = [id]
        mycursor.execute(sql, sql_param)
        result = mycursor.fetchall()

        # except:
        #     print("redirect gaat fout")
        #     return render_template("index.html")

    return render_template("index.html")

@app.route("/verify", methods=["POST", "GET"])
def verify(rando_nr):

    try:
        print("OK1")
        if request.method == "GET":
            print("OK2")
            verify_input = request.form["verify_code"]
            print("OK2.1")
            verify_input = int(verify_input)
            print("OK3")
            if rando_nr == verify_input:
                print("OK4")
                return redirect(url_for("welcome"))

    except:
        return render_template("verify.html")

    return render_template("verify.html")

def send_email(reciever_email):
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

    return rando_nr

@app.route("/welcome", methods=["POST", "GET"])
def logged_in():
    return render_template("dashboard.html")

if __name__ == "__main__":
    main()