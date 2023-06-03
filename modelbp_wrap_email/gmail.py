import os
import pickle
import base64
from google.auth.transport.requests import Request  # pip install google-auth-oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build     # pip install google-api-python-client
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials   # pip install google-auth

# Constants
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = '../secrets/client_secret_196341740635-p5j8hmhopb89qhotitjj83ecsidbhr1s.apps.googleusercontent.com.json'
TOKEN_FILE = 'token.pickle'

def get_auth():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_message(sender, to, subject, message_text):
    message = {
        'raw': base64.urlsafe_b64encode(
            f"From: {sender}\r\n"
            f"To: {to}\r\n"
            f"Subject: {subject}\r\n\r\n"
            f"{message_text}".encode("utf-8")
        ).decode("utf-8")
    }
    return message

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        print("Message sent successfully!")
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")


def send_email(sender, to, subject, message_text, creds=None):
    if creds is None:
        creds = get_auth()

    # Create Gmail service
    service = build('gmail', 'v1', credentials=creds)

    message = create_message(sender, to, subject, message_text)

    # Send the email
    send_message(service, 'me', message)


def main():
    # Authenticate
    creds = get_auth()

    # Create Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Compose the email
    sender = 'rob@papersread.org'
    to = 'kjartan.papersread@gmail.com'
    subject = 'Test Email'
    message_text = 'Hello, this is a test email sent using the Gmail API SDK.'

    message = create_message(sender, to, subject, message_text)

    # Send the email
    send_message(service, 'me', message)

if __name__ == '__main__':
    main()
