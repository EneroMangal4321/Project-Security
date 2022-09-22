# This file is here to test 2FA for our website.
from flask import Flask, url_for, request, render_template
from flask_mail import Mail, Message
import random

app = Flask(__name__)
mail = Mail(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'authenticator@gmail.com'
# app.config['MAIL_PASSWORD'] = ''
# # app.config['MAIL_USE_TLS'] = False
# # app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

@app.route("/")
def main():
    rand_num = random.randint(1000, 9999)

    if request.method == "POST":
        reciever = request.form["name"]

        msg = Message("Verificatie code", sender = 'authenticator@gmail.com', recipients = reciever)
        msg.body = f"goeiedag, uw verificatiecode is {rand_num}"
        mail.send(msg)

        return render_template(url_for("verify")), rand_num

    return render_template("index.html")

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
    app.run()