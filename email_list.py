from smtplib import SMTP
import click
import pandas as pd
from email.mime.text import MIMEText

config = pd.read_csv("config.csv")

# python email_list --except malte
@click.command()
@click.option('--exclude', default=None, help="Don't send to this person")
def main(exclude):
    print(", ".join(config[lambda x: x['first'].str.lower()!=exclude.lower()]['mail'].to_list()))
    
if __name__ == "__main__":
    main()