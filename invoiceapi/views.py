from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from invoiceapi.models import users
from module import func

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                userid = event.source.user_id
                if not users.objects.filter(uid=userid).exists():
                    unit = users.objects.create(uid=userid, state='no')
                    unit.save()
                mtext = event.message.text
                if mtext == '@巴哈勇者福利社':
                    func.sendText1(event)
                    
                elif mtext == '@動漫通':
                    func.sendText2(event)  
                    
                elif mtext == '@動漫通1':
                    func.sendText3(event)      
                    
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
