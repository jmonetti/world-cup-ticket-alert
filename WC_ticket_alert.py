import requests
import json
import sched, time
import smtplib

# Function to send email alert from Gmail if tickets are found
def send_email():   
    to = 'to_email'
    gmail_user = 'from_email'
    gmail_pwd = 'gmail_password'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Tickets! \n'
    print header
    msg = header + '\n There are tickets available! \n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()

# Function to look for semi-final or final tickets in Rio     
def get_final_tix(sc):
    tix_data = requests.get("http://fwctickets.fifa.com/TopsAkaCalls/Calls.aspx/getBasicDataAvaDem?l=en&c=BRA")
    tix = tix_data.text
    tx = json.loads(tix)
    codes = json.loads(tx["d"]["data"])
    lists = codes["BasicCodes"]["PRODUCTPRICES"]
    semi, final = lists[-49:-42], lists[-7:-1] # Games in Rio on Jul. 4 and 13
    for s, f in zip(semi, final):
        quantS, quantF = int(s["Quantity"]), int(f["Quantity"])
        if quantS > 0 or quantF > 0:
            print "Tickets available in Rio!!!"
            send_email()
    sc.enter(600, 1, get_final_tix, (sc,))        

s = sched.scheduler(time.time, time.sleep)    
s.enter(600, 1, get_final_tix, (s,))
s.run()