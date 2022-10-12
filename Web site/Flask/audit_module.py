import os
import time

#This function appends to the audit file. It takes the username and the action to create 
# a formatted audit log. It will log the following: account creation, 
#   failed log in attempts.
def audit(username, action):
    #List with actions (the index of each action equals the number):
    action_list =  ["Account created", "Account creation failed", "User logged in", 
                    "Failed login attempt"]

    #This is the location of the audit file. 
    #On your locale system must change in your locale folder adress.
    audit_file = r'/Users/hadi/Desktop/Blok05/01- Project Security/Group PS - github/Project-Security/Web site/Flask/audit.log'

    os.path.isfile(audit_file)

    current_time = time.localtime(time.time())
    current_time_formatted = time.strftime("%y/%m/%d %H:%M GMT", current_time)

    #Open the audit file with the append mode.
    audit = open(audit_file, 'a')
    audit.write(f'{username}:{action_list[action]} at {current_time_formatted} \n')
    audit.close()

    return