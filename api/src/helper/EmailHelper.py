import re
from email.header import decode_header

from python_helper import Constant as c
from python_framework import Helper, HelperMethod
from python_helper import log, ObjectHelper


SUBJECT = 'Subject'
ORIGIN = 'From'


@Helper()
class EmailHelper:

    @HelperMethod()
    def clean(self, text):
        return c.BLANK.join(charactere if charactere.isalnum() else c.UNDERSCORE for charactere in text)


    @HelperMethod()
    def getAllBetweenCharacters(self, text, firstCharacter, secontCharacter):
        content = text
        try:
            regexpAsString = f'.*?\{firstCharacter}(.*){secontCharacter}.*'
            match = re.search(regexpAsString, text)
            content = match.group(1)
        except Exception as exception:
            log.debug(self.getAllBetweenCharacters, f'Not possible to parse "{content}" properly. Returning it as a string by default', exception=exception, muteStackTrace=True)
        return content


    @HelperMethod()
    def getSubject(self, messageContent):
        log.status(self.getSubject, f'''Getting subject: {messageContent.get(SUBJECT)}''')
        a, b = decode_header(messageContent.get(SUBJECT))[0]
        completeSubject = [(a, b)]
        log.status(self.getSubject, f'Subject: "{completeSubject}"')
        subject = completeSubject[0][0]
        encoding = completeSubject[0][1]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding)
        log.status(self.getSubject, f'Parsed subject: "{subject}"')
        return subject


    @HelperMethod()
    def getOrigin(self, messageContent):
        log.status(self.getOrigin, f'''Getting origin: {messageContent.get(ORIGIN)}''')
        completeOrigin = decode_header(messageContent.get(ORIGIN))
        log.prettyPython(self.getOrigin, f'Origin', completeOrigin, logLevel=log.STATUS)
        try:
            origin = completeOrigin[-1][0]
            encoding = completeOrigin[1][-1]
            if ObjectHelper.isNone(origin):
                origin = completeOrigin[0][0]
            if ObjectHelper.isNone(encoding):
                encoding = completeOrigin[0][-1]
        except Exception as exception:
            log.debug(self.getOrigin, f'Not possible to properly parse origin from "{completeOrigin}". Trying again', exception=exception, muteStackTrace=True)
            # origin = completeOrigin[0][0]
            # encoding = completeOrigin[0][-1]
        if ObjectHelper.isNone(origin):
            origin = 'no.one@send.it'
        if ObjectHelper.isNone(encoding):
            encoding = c.UTF_8
        if isinstance(origin, bytes):
            origin = origin.decode(encoding)
        origin = self.getAllBetweenCharacters(str(origin), c.LESSER, c.BIGGER)
        log.status(self.getOrigin, f'Parsed origin: "{origin}"')
        return origin
