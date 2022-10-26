# 1 If client is banned, redirect, if not, login
# 2 Get client ip adress when pressing login button
# 3 Log client ip adress in database

# 4 Log login attempt of ip adress in database
# 5 If login attempts exceed 5 times, client ip gets banned in database
# 6 After 5 minutes, client ip gets removed from database

from flask import Flask
from flask import request
import socket
import mysql.connector

app = Flask(__name__)

# Connect to database
banneddb = mysql.connector.connect(host="127.0.0.1", port="3306", user="root", password="root", database="banned_db")

bannedcursor = banneddb.cursor(buffered=True)

# Get client IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print("Your IP is: " + ip_address)

# Pre client IP register check
bannedcursor.execute("SELECT ip_address FROM banned_table")

ip_list = bannedcursor.fetchall()

for i in ip_list:
    a = str(i)
    ip_list =a.split(",")[0]
    print(ip_list)

if ip_address in ip_list:
    print("Ip exists in banlist")
else:
    # Registers client IP to database
    query = "INSERT INTO banned_table (ip_address, banned, login_count) VALUES (%s, %s, %s)"
    bannedcursor.execute(query,(ip_address, 0, 0, ))
    banneddb.commit()
    print("Ip Inserted")

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=8000)