import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def send(filename):
    from_mail = "cgong701@gmail.com"
    to_mail = "gongcchen999@gmail.com"
    subject = "Today's stock information from Python"

    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject

    body = "<b>Here is today's stocks information scraped by python</b>"
    msg.attach(MIMEText(body, "html"))

    #filename = "stockinfo.csv"
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    msg.attach(part)
    message = msg.as_string()

    print("Please enter password:")
    password = input()
    
    #set up the gmail server and the app password
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_mail, password)
    server.sendmail(from_mail, to_mail, message)
    server.quit()