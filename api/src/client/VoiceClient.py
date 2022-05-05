from python_framework import HttpClient, HttpClientMethod


from config import VoiceClientConfig


@HttpClient(
    url = VoiceClientConfig.BASE_URL,
    timeout = VoiceClientConfig.DEFAULT_TIMEOUT_IN_SECONDS,
    headers = {
        'Api-Key': f'Bearer {VoiceClientConfig.API_KEY}'
    }
    , logRequest = True,
    logResponse = True
)
class VoiceClient :

    @HttpClientMethod(
        url = '/speech',
        requestClass = [[dict]]
        , logRequest = True,
        logResponse = True
    )
    def speakAll(self, dtoList):
        return self.post(body=dtoList)
