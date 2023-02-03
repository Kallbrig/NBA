"""

The entire purpose of this file is to format and send emails.

"""

from datetime import date
import smtplib
from email.message import EmailMessage
from credentials import *
import base64


def send_email(email_text):
    # construct email
    email = EmailMessage()
    email['Subject'] = f'MVP Leaders - {date.today().month}/{date.today().day}/{date.today().year}'

    email['From'] = gmail_api['email']
    email['To'] = receiving_email['email']
    email.set_content(email_text, subtype='html')

    # Send the message via local SMTP server.
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.ehlo()
        s.login(gmail_api['email'], gmail_api['password'])
        s.send_message(email)


def format_email(table_addition, img_addition=None):
    with open('email_message.html', 'r') as f:
        html_string = f.read()
        html_string = html_string.replace('<!-- THIS IS WHERE YOUR MVP DATA GOES -->', table_addition)
        html_string = html_string.replace('<!-- THIS IS WHERE YOUR IMAGE GOES -->', img_addition)

    return html_string


def get_img_to_html(img_png_path, ):
    data_uri = base64.b64encode(open(img_png_path, 'rb').read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{data_uri}">'
