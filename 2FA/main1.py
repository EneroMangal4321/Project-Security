# This file is here to test 2FA for our website.
from flask import Flask, url_for, request, render_template, redirect
# from flask_mail import Mail, Message
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import random

app = Flask(__name__)
# mail = Mail(app)

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

sender_email = "verify.sec.2022@outlook.com"
password_email = "Verify.Sec"

def main():
    if request.method == "POST":
        try:
            reciever = request.form["email"]
            # name = request.form["name"]
            rando_nr = send_email(reciever)
            print(rando_nr)

            return redirect(url_for("verify")), rando_nr

        except:
            return render_template("index.html")

    return render_template("index.html")

def send_email(reciever_email):
    rando_nr = random.randint(1000,9999)
    msg = EmailMessage()
    msg["Subject"] = "Verificatie Code"
    msg["From"] = formataddr(("Verificatie Code", f"{sender_email}"))
    msg["To"] = reciever_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""Beste 'Naam hier',
        Uw verificatie nummer is {rando_nr} gebruik dit nummer om de 2 stap verificatie af te ronden."""
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, reciever_email, msg.as_string())

    return rando_nr

@app.route("/verify")
def check_code(rand_num):
    code = rand_num

    if request.method == "POST":
        user_code = request.form["verify_code"]

        if code == user_code:
            return render_template(url_for("dashboard"))

    return render_template("verify.html")

@app.route("/dashboard")
def dashoard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    send_email(
        reciever_email="enero.mangal@gmail.com"
    )