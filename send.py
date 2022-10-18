from smtplib import SMTP
import click
import pandas as pd
from email.mime.text import MIMEText

config = pd.read_csv("config.csv")

# python send.py --username lmalte --password passw0rd --file 'mail.txt'
@click.command()
@click.option('--host', default='mail.ethz.ch', help='SMTP server hostname')
@click.option('--port', default=587, help='SMTP server port')
@click.option('--username', default=None, help='SMTP username')
@click.option('--password', default=None, help='SMTP password')
@click.option('--file', default=None, help='File containing the message')
@click.option('--recipient', default=None, help='Recipient email address')
def main(host, port, username, password, file, recipient):
    smtp = SMTP(host, port)
    smtp.connect(host, port)

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(username, password)

    sender = f"{username}@ethz.ch"

    if recipient is None:
        recipients = config['first']
    else:
        recipients = [recipient]
        if recipient not in config['first'].to_list():
            raise ValueError("Invalid recipient")

    for recipient in recipients:
        recipient_address = config[lambda x: x['first']==recipient]['mail'].values[0]

        list_of_links = ""
        for row in config[lambda x: x['first']!=recipient].itertuples():
            if not row.finished:
                list_of_links += f"{row.first} {row.last}: {row.link}\n"

        with open(file, "r") as f:
            message = f.read()

        message = message.format(first=recipient, list_of_links=list_of_links)
        mail = MIMEText(message)
        mail['From'] = sender
        mail['To'] = recipient_address
        mail['Subject'] = "It's T-Shirt time!"

        # print(f"Sending mail {message} to {recipient_address}")
        smtp.sendmail(sender, [recipient_address], mail.as_string())
    
if __name__ == "__main__":
    main()