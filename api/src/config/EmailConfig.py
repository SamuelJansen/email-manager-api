import imaplib

from python_helper import log, EnvironmentHelper
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

USERNAME = globalsInstance.getSetting('email.username')
PASSWORD = globalsInstance.getSetting('email.password')
FETCH_TYPE = '(RFC822)'
SSL_PORT = imaplib.IMAP4_SSL_PORT
IMAP_MAIL = 'imap.gmail.com'
FOLDER_NAME = f'api{EnvironmentHelper.OS_SEPARATOR}src{EnvironmentHelper.OS_SEPARATOR}view'
