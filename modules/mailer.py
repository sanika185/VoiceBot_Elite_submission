import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body,
               from_email="setuvani0@gmail.com",
               password="VaniSetu@2000"):
    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)
