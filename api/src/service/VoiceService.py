from python_helper import Constant as c
from python_helper import EnvironmentHelper, ObjectHelper, RandomHelper, StringHelper, log
from python_framework import Service, ServiceMethod, EnumItem


@Service()
class VoiceService :

    @ServiceMethod(requestClass=[[str], EnumItem])
    def speakAll(self, textList, voice) :
        serviceReturn = None
        try:
            serviceReturn = self.emitter.voice.speakAll([
                {
                    'text': text,
                    'voice': voice
                } for text in textList
            ])
        except Exception as exception:
             log.warning(self.speakAll, 'Not possible to speak', exception=exception, muteStackTrace=True)
        return serviceReturn

    @ServiceMethod(requestClass=[str, EnumItem])
    def simpleSpeak(self, text, voice):
        serviceReturn = None
        try:
            serviceReturn = self.speakAll([text])
        except Exception as exception:
             log.warning(self.simpleSpeak, 'Not possible to speak', exception=exception, muteStackTrace=True)
        return serviceReturn

    @ServiceMethod(requestClass=[str])
    def getConstantNameAsSpeech(self, enumName) :
        serviceReturn = None
        try:
            serviceReturn = StringHelper.join(self.getConstantNameAsSpeechList(enumName), character=c.SPACE)
        except Exception as exception:
             log.warning(self.getConstantNameAsSpeech, 'Not possible to parse name as speech', exception=exception, muteStackTrace=True)
        return serviceReturn

    @ServiceMethod(requestClass=[str])
    def getConstantNameAsSpeechList(self, enumName) :
        serviceReturn = None
        try:
            serviceReturn = [] if ObjectHelper.isNone(enumName) else enumName.lower().split(c.UNDERSCORE)
        except Exception as exception:
             log.warning(self.getConstantNameAsSpeechList, 'Not possible to parse constant as speech list', exception=exception, muteStackTrace=True)
        return serviceReturn
