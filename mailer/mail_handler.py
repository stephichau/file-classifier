import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()

class Mailer:
    def __init__(self, server='localhost', sender='default'):
        # FROM: sender@server
        self._server = smtplib.SMTP(server)
        self._from = sender
    
    def send_mail(self, content: MIMEMultipart, mail_list: list):
        self._server.sendmail(self._from, mail_list, content.as_string(), mail_options=['SMTPUTF8'])

    def stop_server(self):
        self._server.quit()

class Email:
    def __init__(self, sender='', subject='', text_body='', attachments=[], *args, **kw):
        """
        subject: email subject
        text_body: text that will appear in email
        attachments: [(path_to_file, file)] array of tuples of strings
        """
        self._from = sender
        self._subject = subject
        self._text_body = MIMEText(text_body)
        self._attachments = attachments
        self._email = MIMEMultipart()

    @staticmethod
    def join_list(text, _list) -> list:
        return text.join(_list)
        
    def create_content(self, receiver_list: list, cc_list: list) -> None:
        self._email['Subject'] = self._subject
        self._email['From'] = self._from
        self._email['To'] = Email.join_list(', ', receiver_list)
        self._email['CC'] = Email.join_list(', ', cc_list) if cc_list else ''
        
        self._email.attach(self._text_body)
        
        if self._attachments:
            attachments = self.create_attachments()
            list(map(lambda attachment: self._email.attach(attachment), attachments))
    
    def create_attachments(self) -> list:
        attachment_list = [None for _ in range(len(self._attachments))]
        for index in range(len(self._attachments)):
            (path, file) = self._attachments[index]
            attachment = MIMEBase('application', 'octet-stream')
            file_path = '{0}/{1}'.format(path, file)
            _file_bytes = open(file_path, 'rb').read()
            attachment.set_payload(_file_bytes)
            
            encoders.encode_base64(attachment)
            
            attachment.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file))
            attachment_list[index] = attachment
        return attachment_list

