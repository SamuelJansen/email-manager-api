from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


EMITTER_URL = globalsInstance.getSetting('queue.queue-manager-api.emitter.url')
VOICE_MANAGER_API_QUEUE_SPEECH = globalsInstance.getSetting('queue.queue-manager-api.queue.voice-manager-api.speech.key')
EMAIL_MANAGER_API_API_KEY = globalsInstance.getSetting('queue.queue-manager-api.email-manager-api.api-key')
EMITTER_TIMEOUT = globalsInstance.getSetting('queue.queue-manager-api.emitter.timeout')
