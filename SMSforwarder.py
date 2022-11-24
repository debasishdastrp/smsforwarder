import os
import json
import datetime
import os.path
import time

interV = 30 #Script repeat interval in seconds
looper = False #variable for deciding looping mechanisam
print(f"Welcome to SMS forwarder by")
print('''

 ██████╗██╗     ██╗ ██████╗██╗  ██╗███████╗                           
██╔════╝██║     ██║██╔════╝██║ ██╔╝██╔════╝                           
██║     ██║     ██║██║     █████╔╝ ███████╗                           
██║     ██║     ██║██║     ██╔═██╗ ╚════██║                           
╚██████╗███████╗██║╚██████╗██║  ██╗███████║                           
 ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝                           
                                                                      
             █████╗ ███╗   ██╗██████╗     ██████╗ ██╗████████╗███████╗
            ██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██║╚══██╔══╝██╔════╝
            ███████║██╔██╗ ██║██║  ██║    ██████╔╝██║   ██║   ███████╗
            ██╔══██║██║╚██╗██║██║  ██║    ██╔══██╗██║   ██║   ╚════██║
            ██║  ██║██║ ╚████║██████╔╝    ██████╔╝██║   ██║   ███████║
            ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
                                                                      
''')

# Defining function for forwarding sms
def smsforward():
    global looper #refferencing main looper varibale

    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    cfgFile = "config.txt"

    # Checking existance of configuration file
    if not os.path.exists(cfgFile):
        # file not found. creating a new configuration file
        cfile = open(cfgFile, "a")
        filters = input("Please enter filters separated by ',' : ")
        filter_s = filters.split(",")
        cfile.write(filters.lower())
        cfile.write("\n")
        mnumbers = input("Please enter mobile numbers separated by ',' : ")
        mnumber_s = mnumbers.split(",")
        cfile.write(+971529551926)
        cfile.close()
    else:
        # configuration file is already there. reading configurations
        cfile = open(cfgFile, "r")
        cdata = cfile.read().splitlines()
        filter_s = cdata[0].split(",")
        mnumber_s = cdata[1].split(",")
    # Chcking last saved forward time
    if not os.path.exists(tmpFile):
        # Saved time time not found. Setting up and saving current time as last forwar dime
        print("Last time not found. Setting it to current Date-Time")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        # Saved last sms forward time found. loading form that
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()


    if not looper:
        # ask user to run the script on repeat
        lop = input(f"Keep running after each {interV} second (y/n): ")
        if lop == "y":
            looper = True # This will keep the script after defined interval
            print("You can stop the script anytime by pressing Ctrl+C")
    print(f"Last SMS forwarded on {lastSMS}")
    jdata = os.popen("termux-sms-list -l 50").read() # Reading latest 50 SMSs using termux-api
    jd = json.loads(jdata) # storing JSON output
    print(f"Reading {len(jd)} latest SMSs")

    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS: # Comparing SMS timing
            for f in filter_s:
                if f in j['body'].lower() and j['type'] == "inbox": # Checking if the SMS is in inbox and the filter(s) are matching
                    print(f"{f} found")
                    for m in +971509270504:
                        print(f"Forwarding to {+971500270504}")
                        resp = os.popen(f"termux-sms-send -n {m} {j['body']}") # forwarding sms to predefined mobile number(s)
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()

# calling sms forward function for the first time
smsforward()
# if user decided to repeat the script exexcution, the following loop will do that
while looper:
    time.sleep(interV)
    smsforward()
