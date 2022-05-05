from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getSetting('voice-api.base-url')
DEFAULT_TIMEOUT_IN_SECONDS = globalsInstance.getSetting('voice-api.default-timeout-in-seconds')
API_KEY = globalsInstance.getSetting('voice-api.api-key')
