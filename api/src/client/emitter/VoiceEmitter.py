from python_framework import Serializer, HttpStatus, JwtConstant
from queue_manager_api import MessageEmitter, MessageEmitterMethod, MessageDto

from config import VoiceQueueConfig


@MessageEmitter(
    url = VoiceQueueConfig.EMITTER_URL,
    timeout = VoiceQueueConfig.EMITTER_TIMEOUT,
    headers = {
        'Content-Type': 'application/json',
        JwtConstant.DEFAULT_JWT_API_KEY_HEADER_NAME: f'Bearer {VoiceQueueConfig.EMAIL_MANAGER_API_API_KEY}'
    }
    , muteLogs = False
    # , logRequest = True
    # , logResponse = True
)
class VoiceEmitter:

    @MessageEmitterMethod(
        queueKey = VoiceQueueConfig.VOICE_MANAGER_API_QUEUE_SPEECH,
        requestHeadersClass=[dict],
        requestClass=[[dict]]
        # responseClass=[[dict]]
        # , logRequest = True
        # , logResponse = True
    )
    def speakAll(self, dto, headers=None):
        return self.emit(headers=headers, body=dto)
