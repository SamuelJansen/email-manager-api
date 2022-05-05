from python_framework import Controller, ControllerMethod, HttpStatus, EnumItemStr


from enumeration.ApiKeyContext import ApiKeyContext
import EmailDto


@Controller(url = '/content', tag='Email', description='Email controller', logRequest=True, logResponse=True)
class EmailController:

    @ControllerMethod(url='/',
        requestParamClass=[EmailDto.EmaiContentRequestParamsDto],
        responseClass=[[dict]],
        apiKeyRequired=[ApiKeyContext.USER, ApiKeyContext.API]
    )
    def get(self, params=None):
        return self.service.email.getMessages(params), HttpStatus.OK
