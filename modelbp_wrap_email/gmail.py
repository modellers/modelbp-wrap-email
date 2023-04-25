"""
Sends email using Gmail API

More information
https://mailtrap.io/blog/python-send-email-gmail/ (section: How to send an email with Python via Gmail API?)
"""

import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import os, sys
import argparse

def get_auth():
    SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
    # get credentials from file in secrets folder if it exists
    if os.path.exists('../secrets/gmail_credential.json'):
        flow = InstalledAppFlow.from_client_secrets_file('../secrets/gmail_credential.json', SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        # get credentials from environment variables if they exist
        config = {
            "installed": {
                "client_id": os.environ.get("GMAIL_CLIENT_ID"),
                "project_id": os.environ.get("GMAIL_PROJECT_ID"),
                "auth_uri": os.environ.get("GMAIL_AUTH_URI"),
                "token_uri": os.environ.get("GMAIL_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("GMAIL_AUTH_PROVIDER_X509_CERT_URL"),
                "client_secret": os.environ.get("GMAIL_CLIENT_SECRET"),
                "redirect_uris": os.environ.get("GMAIL_REDIRECT_URIS")
            }
        }
        # check if credentials are valid
        if config["installed"]["client_id"] is None:
            print("No credentials found. Expected to find them in secrets/gmail_credential.json or environment variables.")
            sys.exit(1)
        # create flow
        flow = InstalledAppFlow.from_client_config(config, SCOPES)
        # get credentials
        creds = flow.run_local_server(port=0)

    return creds

def sendText(message, to_email, credentials):
    service = build('gmail', 'v1', credentials=credentials)
    message = MIMEText('This is the body of the email')
    message['to'] = to_email
    message['subject'] = 'Test'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

if __name__ == '__main__':
    credentials = get_auth()
    # using arg parser to get arguments
    parser = argparse.ArgumentParser(description='Send email using Gmail API')
    parser.add_argument('-m', '--message', help='Message to send', required=False)
    parser.add_argument('-t', '--to', help='Email address to send to', required=False)
    args = parser.parse_args()
    if args.message and args.to:
        sendText(message=args.message, to_email=args.to, credentials=credentials)
