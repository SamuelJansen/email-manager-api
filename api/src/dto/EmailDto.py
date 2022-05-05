from python_framework import ConverterStatic

from constant import ContentConstant


class EmaiContentRequestParamsDto:
    def __init__(self,
        amount = None,
        origin = None,
        emailBox = None
    ):
        self.amount = int(ConverterStatic.getValueOrDefault(
            amount,
            ContentConstant.DEFAULT_MESSAGE_AMOUNT
        ))
        self.origin = origin
        self.emailBox = emailBox
