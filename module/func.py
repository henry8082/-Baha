from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,CarouselTemplate,URITemplateAction,CarouselColumn,FlexSendMessage

import requests
try:
    from bs4 import BeautifulSoup as bs
except :
    pass

import re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from invoiceapi.models import users

import urllib
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendText1(event):  #傳送文字
    try:
        url = "https://fuli.gamer.com.tw/shop.php"

        
        res = requests.get(url).text
        
        textall = re.compile(r'''(<a class="items-card" href="(.+)">
<div class="card-content">
<div class="card-left flex-center">
<img src="(.+)" alt="(.+)">
</div>
<div class="card-right">
<h2 class="items-title">(.+)</h2>
<div class="items-instructions">
<p>(.+)<span> (.+)</span></p>
<p>(.+)<span> (.+)</span></p>
</div>
<div class="items-instructions">
<p>
(.+)
<span> (.+)</span>
</p>
</div>
<div class="items-instructions">
<span class="type-tag ">(.+)</span>
<div class="price"><p class="digital">(.+)</p>(.+)</div>
</div>
<div class="flex-center card-btn c-primary">(.+)</div>
</div>
</div>
</a>)''')
        
        findalltext = textall.findall(res)

        content_bubble = []
        for i in findalltext:
            content_bubble.append(
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "url": i[2],
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "20:20"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": i[3],
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[5],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[6],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "align": "start",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[7],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[8],
                        "wrap": True,
                        "color": "#FF0000",
                        "size": "sm",
                        "flex": 5,
                        "align": "start",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[9],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[10],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "gravity": "center",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[11],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[12]+i[13],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "weight": "bold"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "link",
                "action": {
                  "type": "uri",
                  "label": i[14],
                  "uri": i[1]
                },
                "color": "#FFFFFF",
                "height": "sm"
              },
              {
                "type": "spacer",
                "size": "sm"
              }
            ],
            "flex": 0,
            "backgroundColor": "#0000ff"
          }
        })
        
        bubble = {"type": "carousel","contents":content_bubble}
        message = FlexSendMessage(alt_text="巴哈勇者福利社", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendText3(event):  #傳送文字
    try:
        url = "https://fuli.gamer.com.tw/shop.php"

        
        res = requests.get(url)
        
        soup = bs(res.text,'lxml')
        find_all_a = soup.find_all('a','items-card')
        listall = []
        for i in find_all_a:
            title = i.find('h2','items-title').text
            href = i['href']
            alltext = i.find_all('div','items-instructions')
            print(f'{title}\n{href}')
            row = []
            row.append(title)
            row.append(href)
            for j in alltext:
                if '商品數量' in j.text:
                    print(j.text.strip('\n').replace(' ',':'))
                    row.append(j.text.strip('\n').replace(' ',':'))
                else:
                    row.append(j.text.strip('\n').replace('\n',':'))
                    print(j.text.strip('\n').replace('\n',':'))
            print("---------------------")
            listall.append(row)

        content_bubble = []
        for i in listall:
            content_bubble.append(
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "url": i[2],
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "20:20"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": i[0],
                "weight": "bold",
                "size": "xl",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[3].split(' ')[0],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[3].split(' ')[1],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "align": "start",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[4].split(' ')[0],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[4].split(' ')[1],
                        "wrap": True,
                        "color": "#FF0000",
                        "size": "sm",
                        "flex": 5,
                        "align": "start",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[5].split(':')[0],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[5].split(':')[1],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "gravity": "center",
                        "weight": "bold"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": i[6].split(':')[0],
                        "color": "#000000",
                        "size": "sm",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": i[6].split(':')[1],
                        "wrap": True,
                        "color": "#2300D1",
                        "size": "sm",
                        "flex": 5,
                        "weight": "bold"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "link",
                "action": {
                  "type": "uri",
                  "label": "商品連結",
                  "uri": i[1]
                },
                "color": "#FFFFFF",
                "height": "sm"
              },
              {
                "type": "spacer",
                "size": "sm"
              }
            ],
            "flex": 0,
            "backgroundColor": "#0000ff"
          }
        })
        
        bubble = {"type": "carousel","contents":content_bubble}
        message = FlexSendMessage(alt_text="巴哈勇者福利社", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendText2(event):  #傳送文字
    try:
        url = "https://fuli.gamer.com.tw/shop.php"

        res = requests.get(url)
        
        soup = bs(res.text,'lxml')
        find_all_a = soup.find_all('a','items-card')
                
        message = [TextSendMessage(  
            text = find_all_a[0].text),
TextSendMessage( text = find_all_a[1].text),TextSendMessage(  
            text = find_all_a[2].text)]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendUse(event):  #使用說明
    try:
        text1 ='''
1. 「對獎」功能會提示使用者輸入發票最後三碼，若最後三碼有中獎，就提示使用者輸入發票前五碼。
2. 為方便使用者輸入，也可以直接輸入發票最後三碼直接對獎 (不需按「對獎」項目)。
3. 「前期中獎號碼」功能會顯示前兩期發票中獎號碼。
4. 「本期中獎號碼」功能會顯示最近一期發票中獎號碼。
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def showCurrent(event):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)  #解析XML
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        title = items[0][0].text  #期別
        ptext = items[0][2].text  #中獎號碼
        ptext = ptext.replace('<p>','').replace('</p>','\n')
        message = title + '月\n' + ptext[:-1]  #ptext[:-1]為移除最後一個\n
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))

def showOld(event):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)  #解析XML
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        message = ''
        for i in range(1,3):
            title = items[i][0].text  #期別
            ptext = items[i][2].text  #中獎號碼
            ptext = ptext.replace('<p>','').replace('</p>','\n')
            message = message + title + '月\n' + ptext + '\n'
        message = message[:-2]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))

def show3digit(event, mtext, userid):
    try:
        content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
        tree = ET.fromstring(content.text)
        items = list(tree.iter(tag='item'))  #取得item標籤內容
        ptext = items[0][2].text  #中獎號碼
        ptext = ptext.replace('<p>','').replace('</p>','')
        temlist = ptext.split('：')
        prizelist = []  #特別獎或特獎後三碼
        prizelist.append(temlist[1][5:8])
        prizelist.append(temlist[2][5:8])
        prize6list1 = []  #頭獎後三碼六獎中獎號碼
        for i in range(3):
            prize6list1.append(temlist[3][9*i+5:9*i+8])
        prize6list2 = temlist[4].split('、')  #增開六獎
        unit = users.objects.get(uid=userid)
        unit.state = 'no'
        unit.save()
        if mtext in prizelist:
            message = '符合特別獎或特獎後三碼，請繼續輸入發票前五碼！'
            unit = users.objects.get(uid=userid)
            unit.state = 'special'
            unit.save()
        elif mtext in prize6list1:
            message = '恭喜！至少中六獎，請繼續輸入發票前五碼！'
            unit = users.objects.get(uid=userid)
            unit.state = 'head'
            unit.save()
        elif mtext in prize6list2:
            message = '恭喜！此張發票中了六獎！'
        else:
            message = '很可惜，未中獎。請輸入下一張發票最後三碼。'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))

def show5digit(event, mtext, userid):
    try:
        unit = users.objects.get(uid=userid)
        mode = unit.state
        if mode == 'no':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請先輸入發票最後三碼！'))
        else:
            try:
                content = requests.get('http://invoice.etax.nat.gov.tw/invoice.xml')
                tree = ET.fromstring(content.text)  #解析DOM
                items = list(tree.iter(tag='item'))  #取得item標籤內容
                ptext = items[0][2].text  #中獎號碼
                ptext = ptext.replace('<p>','').replace('</p>','')
                temlist = ptext.split('：')
                special1 = temlist[1][0:5]  #特別獎前五碼
                special2 = temlist[2][0:5]  #特獎前五碼
                prizehead = []  #頭獎前五碼
                for i in range(3):
                    prizehead.append(temlist[3][9*i:9*i+5])
                sflag = False  #記錄是否中特別獎或特獎
                if mode=='special' and mtext==special1:
                    message = '恭喜！此張發票中了特別獎！'
                    sflag = True
                elif mode=='special' and mtext==special2:
                    message = '恭喜！此張發票中了特獎！'
                    sflag = True
                if mode=='special' and sflag==False:
                    message = '很可惜，未中獎。請輸入下一張發票最後三碼。'
                elif mode=='head' and sflag==False:
                    if checkhead(mtext, prizehead[0], prizehead[1], prizehead[2]):
                        message = '恭喜！此張發票中了頭獎！'
                    elif checkhead(mtext[1:5], prizehead[0][1:5], prizehead[1][1:5], prizehead[2][1:5]):
                        message = '恭喜！此張發票中了二獎！'
                    elif checkhead(mtext[2:5], prizehead[0][2:5], prizehead[1][2:5], prizehead[2][2:5]):
                        message = '恭喜！此張發票中了三獎！'
                    elif checkhead(mtext[3:5], prizehead[0][3:5], prizehead[1][3:5], prizehead[2][3:5]):
                        message = '恭喜！此張發票中了四獎！'
                    elif checkhead(mtext[4], prizehead[0][4], prizehead[1][4], prizehead[2][4]):
                        message = '恭喜！此張發票中了五獎！'
                    else:
                        message = '恭喜！此張發票中了六獎！'
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
                unit = users.objects.get(uid=userid)
                unit.state = 'no'
                unit.save()
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='讀取發票號碼發生錯誤！'))
    except:
        unit = users.objects.get(uid=userid)
        unit.state = 'no'
        unit.save()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='模式文字檔讀取錯誤！'))

def checkhead(mtext, str1, str2, str3):
    return (mtext==str1 or mtext==str2 or mtext==str3)
