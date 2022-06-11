import os
import json
import datetime
import os.path
import time

interV = 30
looper = False
print(f"Welcome to SMS forwarder by Clicks and Bits")


def smsforward():
    global looper

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
        cfile.write(mnumbers)
        cfile.close()
    else:
        # configuration file is already there. reading configurations
        cfile = open(cfgFile, "r")
        cdata = cfile.read().splitlines()
        filter_s = cdata[0].split(",")
        mnumber_s = cdata[1].split(",")

    if not os.path.exists(tmpFile):
        print("Last time not found. Setting it to current Date-Time")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()

    if not looper:
        lop = input(f"Keep running after each {interV} second (y/n): ")
        if lop == "y":
            looper = True
    print(f"Last SMS checked on {lastSMS}")
    jdata = os.popen("termux-sms-list -l 50").read()
    jd = json.loads(jdata)
    print(f"{len(jd)} SMSs available")

    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS:
            for f in filter_s:
                if f in j['body'].lower() and j['type'] == "inbox":
                    print(f"{f} found")
                    for m in mnumber_s:
                        print(f"Forwarding to {m}")
                        resp = os.popen(f"termux-sms-send -n {m} {j['body']}")
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()


smsforward()

while looper:
    time.sleep(interV)
    smsforward()
