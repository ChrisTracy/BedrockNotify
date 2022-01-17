#import packages
import os
import glob
import requests
import time

#Set variables from env
webhook_url = os.environ['WEBHOOK']
interval = os.environ['INTERVAL']
interval = int(interval)

#Start loop
while True:

    #init array
    connected = []

    # Pull  log files
    list_of_files = glob.glob('/MClogs/*') 
    latest_file = max(list_of_files, key=os.path.getctime)

    #Open last Log and Check for login
    file = open(latest_file, 'r')
    Lines = file.readlines()

    #Loop lines and add connected players to array
    for Line in Lines:
        if "Player connected" in Line or "Player disconnected" in Line:
            connected.append(Line)

    #If connected contains information move on
    if connected:

        #Get last connected
        array_length = len(connected)
        last_connected = connected[array_length - 1]

        #Check lastsent file to prevent double notif
        last_sent = open('/app/last_sent.txt', 'r').read()

        #Compare and send if they don't match
        if last_connected in last_sent:
            print("No new login found in Logs")
        else:
            print("New Login detected in Logs")
            #Write out to check next time
            baw = open("/app/last_sent.txt", "w")
            baw.write(last_connected)
            baw.close()

            #Format nicely for Discord
            split_string_front = last_connected.split("INFO] ", 1)
            substring_front = split_string_front[1]
            split_string_back = substring_front.split(", ", 1)
            DiscordMessage = split_string_back[0]
            print(DiscordMessage)

            #Send to Discord
            Message = {
                "content": DiscordMessage
            }
            requests.post(webhook_url, data=Message)
        #clear variables
        connected = ""
        last_connected = ""

    #sleep while loop
    time.sleep(interval)
