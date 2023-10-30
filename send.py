from smtplib import SMTP
import click
import pandas as pd
from email.mime.text import MIMEText

config = pd.read_csv("config.csv")

for row in config.itertuples():
    if row.mail != f"{row.first.lower()}.{row.last.lower()}@stat.math.ethz.ch":
        print(f"Mail of {row.first} {row.last} is {row.mail}.")

if config['mail'].nunique() != len(config):
    raise ValueError("Duplicate email addresses found.")

if config['link'].nunique() != len(config):
    raise ValueError("Duplicate links found.")

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
        recipients = config.to_dict("records")
    else:
        raise ValueError
        recipients = [recipient]
        if recipient not in config['first'].to_list():
            raise ValueError("Invalid recipient")

    for recipient in recipients:
        recipient_address = recipient["mail"]

        list_of_links = ""
        for row in config.itertuples():
            if row.mail != recipient_address:
                list_of_links += f"{row.first} {row.last}: {row.link}\n"

        with open(file, "r") as f:
            message = f.read()

        message = message.format(first=recipient['first'], list_of_links=list_of_links)
        mail = MIMEText(message)
        mail['From'] = sender
        mail['To'] = recipient_address
        mail['Subject'] = "Here are (updated) polybox links for PhD t-shirt ideas"

        if recipient_address in message:
            raise ValueError("Recipient address found in message")

        print(f"Sending mail {message} to {recipient_address}")
        smtp.sendmail(sender, [recipient_address], mail.as_string())
    
if __name__ == "__main__":
    main()