from python_helper import Constant as c
from python_helper import log
from python_framework import Service, ServiceMethod


class FileOperation:
    WRITE_BYTES = 'wb'
    WRITE_TEXT = 'w'
    OVERRIDE_BYTES = '+wb'
    OVERRIDE_TEXT = '+w'


class ContentType:
    TEXT_PLAIN = 'text/plain'
    TEXT_HTML = 'text/html'


@Service()
class EmailService:

    @ServiceMethod()
    def getMessages(self, params):
        return self.processMessages(params.amount, params.origin, params.emailBox)


    @ServiceMethod(requestClass=[int, str, str])
    def processMessages(self, amount, origin, emailBox):
        log.status(self.processMessages, f'Processing {amount} "{emailBox}" mail box messages from "{origin}"')
        self.client.email.login()
        emailException = None
        mailContentList = []
        try:
            messagesAmount, messagesStatus, messages = self.client.email.loadMessages(emailBox)
            for messageIndex in range(messagesAmount, messagesAmount - amount, -1):
                rawMessage = self.client.email.fetchRawMessage(messageIndex)
                mailContentDictionary = {
                    'subject': [],
                    f'{ContentType.TEXT_PLAIN}': [],
                    f'{ContentType.TEXT_HTML}': []
                }
                mailContentList.append(mailContentDictionary)
                for message in rawMessage:
                    if isinstance(message, tuple):
                        self.processMessage(message, origin, mailContentDictionary)
            log.status(self.processMessages, f'Messages processed')
        except Exception as exception:
            emailException = exception
            log.failure(self.processMessages, 'Not possible to processes messages properly', exception=exception, muteStackTrace=True)
        self.client.email.logout()
        if emailException:
            raise emailException
        return mailContentList


    @ServiceMethod()
    def processMessage(self, message, origin, mailContentDictionary):
        log.status(self.processMessage, f'Processing message from {origin}')
        try:
            messageContent = self.client.email.getMessageContent(message)
            messageOrigin = self.helper.email.getOrigin(messageContent)
            messageSubject = self.helper.email.getSubject(messageContent)
            if origin and origin in messageOrigin:
                log.status(self.processMessage, f'Processing message "{messageSubject}" from "{messageOrigin}"')
                if messageContent.is_multipart():
                    self.processMultipartMessage(messageContent, messageSubject, mailContentDictionary)
                else:
                    content_type = messageContent.get_content_type()
                    decodedMessageContent = messageContent.get_payload(decode=True).decode(encoding=c.UTF_8)
                    if ContentType.TEXT_PLAIN == content_type:
                        self.processTextPlainMessage(messageSubject, decodedMessageContent, mailContentDictionary)
                    elif ContentType.TEXT_HTML == content_type:
                        self.processTextHtmlMessage(messageSubject, decodedMessageContent, mailContentDictionary)
        except Exception as exception:
            log.failure(self.processMessage, 'Not possible to processes message properly. Check LOG log level for mor information', exception=exception, muteStackTrace=True)
        log.status(self.processMessage, f'Message processed')
        return mailContentDictionary


    @ServiceMethod()
    def processMultipartMessage(self, messageContent, messageSubject, mailContentDictionary):
        log.status(self.processMultipartMessage, f'Processing multipart "{messageSubject}" message')
        for part in messageContent.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            try:
                decodedMessageContent = part.get_payload(decode=True).decode(encoding=c.UTF_8)
            except Exception as exception:
                decodedMessageContent = str(part)
                log.debug(self.processMultipartMessage, f'Not possible to get message content payload from "{messageSubject}" message', exception=exception, muteStackTrace=True)
            if ContentType.TEXT_PLAIN == content_type and 'attachment' not in content_disposition:
                self.processTextPlainMessage(messageSubject, decodedMessageContent, mailContentDictionary)
            elif 'attachment' in content_disposition:
                filename = part.get_filename()
                if filename:
                    self.client.email.writeContent(
                        filename,
                        self.helper.email.clean(messageSubject),
                        part.get_payload(decode=True),
                        FileOperation.OVERRIDE_BYTES
                    )
            elif ContentType.TEXT_HTML == content_type:
                self.processTextHtmlMessage(messageSubject, decodedMessageContent, mailContentDictionary)
        log.status(self.processMultipartMessage, f'Multipart "{messageSubject}" message processed')


    @ServiceMethod()
    def processTextPlainMessage(self, messageSubject, decodedMessageContent, mailContentDictionary):
        log.status(self.processTextPlainMessage, f'Processing plain text "{messageSubject}" message')
        mailContentDictionary.get(ContentType.TEXT_PLAIN).append(decodedMessageContent)
        log.status(self.processTextPlainMessage, f'Plain text "{messageSubject}" message processed')


    @ServiceMethod()
    def processTextHtmlMessage(self, messageSubject, decodedMessageContent, mailContentDictionary):
        log.status(self.processTextHtmlMessage, f'Processing html text "{messageSubject}" message')
        # self.client.email.writeContent(
        #     'index.html',
        #     self.helper.email.clean(messageSubject),
        #     decodedMessageContent,
        #     FileOperation.OVERRIDE_TEXT
        # )
        mailContentDictionary.get(ContentType.TEXT_HTML).append(decodedMessageContent)
        mailContentDictionary.get('subject').append(self.helper.email.clean(messageSubject))
        log.status(self.processMultipartMessage, f'Html text "{messageSubject}" message processed')
