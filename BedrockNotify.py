import os
import glob
import requests
import time

webhook_url = os.environ['WEBHOOK']
interval = os.environ['INTERVAL']
alerts = os.environ['ALERTS']

#convert interval to int
interval = int(interval)

def LogNotifyInfo(var, type):
    #Get last var
    array_length = len(var)
    last_var = var[array_length - 1]

    #Check lastsent file to prevent double notif
    last_sent = open(f'/app/last_sent_{type}.txt', 'r').read()

    #Compare and send if they don't match
    if last_var in last_sent:
        print(f"New {type} log not detected")
    else:
        print(f"New {type} log detected")
        #Write out to check next time
        baw = open(f"/app/last_sent_{type}.txt", "w")
        baw.write(last_var)
        baw.close()

        #Format nicely for Discord
        split_string_front = last_var.split("INFO] ", 1)
        substring_front = split_string_front[1]
        split_string_back = substring_front.split(", ", 1)
        DiscordMessage = split_string_back[0]
        print(DiscordMessage)

        #Send to Discord
        Message = {
            "content": DiscordMessage
        }
        requests.post(webhook_url, data=Message)


while True:

    #init array
    connected = []
    disconnected = []

    # Pull  log files
    list_of_files = glob.glob('/MClogs/*') 
    latest_file = max(list_of_files, key=os.path.getctime)

    #Open last Log and Check for log
    file = open(latest_file, 'r')
    Lines = file.readlines()

    #Loop lines and add log line to array
    for Line in Lines:
        if "Player connected" in Line:
            connected.append(Line)
        if "Player disconnected" in Line:
            disconnected.append(Line)

    #Check params and send notice
    if "connected" in alerts:
        if connected:
            LogNotifyInfo(var=connected, type="connected")
    if "disconnected" in alerts:
        if disconnected:
            LogNotifyInfo(var=disconnected, type="disconnected")

    #sleep for loop
    time.sleep(interval)
