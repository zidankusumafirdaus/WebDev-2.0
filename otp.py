import random
import smtplib
from flask import session, render_template
from email.message import EmailMessage

def codeotp():
    otp = ""    
    for i in range(6):
        otp += str(random.randint(0,9))
    return otp

def sendotp():
    email = session.get('email')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    from_mail = 'alulawak36@gmail.com'
    server.login(from_mail, 'ixrn eriy toup kigx')
    to_mail = email
        
    message = EmailMessage()
    message['Subject'] = 'OTP Verification'
    message['From'] = from_mail
    message['To'] = to_mail
    
    message.set_content("Your OTP is: " + codeotp())    
    server.send_message(message)
    return render_template("register & otp/index.html")