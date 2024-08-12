import random
import smtplib
from flask import session, render_template
from email.message import EmailMessage

def codeotp():
    otp = ""    
    for i in range(6):
        otp += str(random.randint(0,9))
    return otp

def sendotp(otp_code):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('alulawak36@gmail.com', 'ixrn eriy toup kigx')
        
    message = EmailMessage()
    message['Subject'] = 'OTP Verification'
    message['From'] = 'alulawak36@gmail.com'
    message['To'] = session.get('email')
    
    message.set_content("Your OTP is: " + otp_code)    
    server.send_message(message)