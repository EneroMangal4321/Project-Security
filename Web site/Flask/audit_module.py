import os
import time

#This function appends to the audit file. It takes the username and the action to create 
# a formatted audit log. It will log the following: account creation, account deletion, 
#   failed log in attempts, if a flag is captured and updates to the containers that are running.
def audit(username, action):
    #List with actions (the index of each action equals the number):
    action_list =  ["Account created", "Account creation failed", "User logged in", 
                    "Failed login attempt", "Started a CTF", "Failed to start CTF",
                     "Captured a flag", "Stopped all CTFs running", "Account deleted"]

    #This is the location of the audit file
    audit_file = r'/var/www/ctf/audit.log'

    os.path.isfile(audit_file)

    current_time = time.localtime(time.time())
    current_time_formatted = time.strftime("%y/%m/%d %H:%M GMT", current_time)

    #Open the audit file with the append mode.
    audit = open(audit_file, 'a')
    audit.write(f'{username}:{action_list[action]} at {current_time_formatted} \n')
    audit.close()

    return