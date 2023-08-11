from __future__ import print_function
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import client, file, tools
import codecs

SCOPES = "https://www.googleapis.com/auth/gmail.send"


def gmail_send_message(body,correo,creds):


    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        
        message.set_content(body,'html')

        message['To'] = correo
        message['From'] = 'mateo.bernal.bonil@gmail.com'
        message['Subject'] = 'Evaluacion de criticidad archivos'
        
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message
