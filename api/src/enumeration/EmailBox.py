from python_framework import Enum, EnumItem
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


@Enum()
class EmailBoxEnumeration :
    INBOX = EnumItem()


EmailBox = EmailBoxEnumeration()
