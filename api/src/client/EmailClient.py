import imaplib
import email
import os
import webbrowser

from python_helper import log
from python_framework import Client, ClientMethod

from config import EmailConfig


###- Enable Less Secure Apps
###- https://myaccount.google.com/lesssecureapps?pli=1
###- Enable IMAP
###- https://mail.google.com/mail/u/1/#settings/fwdandpop


class EmailManager:

    def __init__(self, config):
        self.imap = None
        self.config = config
        self.messagesStatus = None
        self.messages = [0]

    def login(self):
        self.imap = imaplib.IMAP4_SSL(self.config.IMAP_MAIL, port=self.config.SSL_PORT)
        self.imap.login(self.config.USERNAME, self.config.PASSWORD)

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def loadMessages(self, emailBox):
        self.messagesStatus, self.messages = self.imap.select(emailBox)
        return self.getMessagesAmount(), self.messagesStatus, self.messages

    def getMessagesAmount(self):
        return int(self.messages[0])

    def fetchRawMessage(self, messageIndex):
        return self.imap.fetch(str(messageIndex), self.config.FETCH_TYPE)

    def writeContent(self, filename, fileUri, content, operation):
        # uri = os.path.join(self.config.FOLDER_NAME, fileUri)
        uri = self.config.FOLDER_NAME
        if not os.path.isdir(uri):
            os.mkdir(uri)
        filepath = os.path.join(uri, filename)
        try:
            open(filepath, operation).write(content)
        except Exception as exception:
            log.failure(self.writeContent, f'Not possible to write content. Content: {content}, operation: {operation}, exception: {exception}')
        webbrowser.open(filepath)
        return filepath

@Client()
class EmailClient:

    manager = EmailManager(EmailConfig)

    # @ClientMethod()
    def login(self):
        return self.manager.login()


    # @ClientMethod()
    def loadMessages(self, emailBox):
        messagesAmount, messagesStatus, messages = self.manager.loadMessages(emailBox)
        return messagesAmount, messagesStatus, messages


    # @ClientMethod()
    def getMessageContent(self, message):
        return email.message_from_bytes(message[1])


    # @ClientMethod()
    def fetchRawMessage(self, messageIndex):
        return self.manager.fetchRawMessage(messageIndex)[1]


    # @ClientMethod()
    def writeContent(self, filename, fileUri, content, operation):
        self.manager.writeContent(filename, fileUri, content, operation)


    # @ClientMethod()
    def logout(self):
        return self.manager.logout()
