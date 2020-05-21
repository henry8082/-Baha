from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,CarouselTemplate,URITemplateAction,CarouselColumn,FlexSendMessage

import requests
import re
from bs4 import BeautifulSoup
#from selenium import webdriver
import os
import datetime
import traceback
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from invoiceapi.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendText1(event):  #查詢勇者福利社
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
<div class="(.+)">(.+)</div>
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
                "type": "filler"
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
                  "label": i[15],
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
          },
          "styles": {
            "footer": {
              "backgroundColor": "#0000E3"
            }
          }
        })
        
        bubble = {"type": "carousel","contents":content_bubble}
        message = FlexSendMessage(alt_text="巴哈勇者福利社", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def sendText2(event):  #傳送動漫通
    try:
        url = 'https://home.gamer.com.tw/creationCategory.php?v=1&owner=blackXblue&c=370818'
        res1 = requests.get(url).text
        
        textall = re.compile('''<tr>
<td align="left"><img src="https://i2.bahamut.com.tw/spacer.gif" class="IMG-C09" /><a href="(.+)">(.+)</a></td>
<td nowrap="nowrap"><a href="//home.gamer.com.tw/blackXblue">X洨妹</a></td>
<td nowrap="nowrap">(.+)</td>
</tr>''')
        findalltext = textall.findall(res1)
        
        # today= datetime.date.today()
        # formatted_today = today.strftime('%m/%d')
        # if formatted_today in findalltext[0][1]:
        url2 = 'https://home.gamer.com.tw/'+findalltext[0][0]
        res2 = requests.get(url2).text
        
        tag = r"""<div>&#91;(.+)&#93;</div><div>(.+)</div><div>(.+)</div><div>(.+)</div><div>(.+)</div><div>(.+)</div><div>(.+)</div><div><br></div><div>(.+)</div></div>"""
        textall2 = re.compile(tag)        
        findalltext2 = textall2.findall(res2)
        if len(findalltext2) ==0:
            textall2 = re.compile(r'''<div class="MSG-list8C">&#91;(.+)&#93;<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<div><br></div><div>(.+)</div></div>''')
            findalltext2 = textall2.findall(res2)
            
        colors = []
        for i in range(3,7):
            if  findalltext2[0][7][-1] == findalltext2[0][i][0]: colors.append(['#FF0000','bold'])
            else:colors.append(["#000000","regular"])

        bubble3 ={
  "type": "bubble",
  "hero": {
    "type": "image",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "url": "https://p2.bahamut.com.tw/HOME/53/creation_blackxblue.PNG"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": findalltext2[0][0],
        "size": "xl",
        "color": "#0000E3",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": findalltext2[0][1],
        "size": "xl",
        "color": "#0008FF",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": findalltext2[0][2],
        "wrap": True,
        "color": "#0008FF",
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": findalltext2[0][3],
                "size": "sm",
                "align": "start",
                "color": colors[0][0],
                "weight": colors[0][1]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": findalltext2[0][4],
                "size": "sm",
                "align": "start",
                "color": colors[1][0],
                "weight": colors[1][1]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": findalltext2[0][5],
                "size": "sm",
                "align": "start",
                "color": colors[2][0],
                "weight": colors[2][1]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": findalltext2[0][6],
                "size": "sm",
                "align": "start",
                "color": colors[3][0],
                "weight": colors[3][1]
              }
            ]
          }
        ]
      }
    ],
    "backgroundColor": "#f9f9f9"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "spacer",
        "size": "xxl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": findalltext2[0][7],
            "size": "xl",
            "align": "center",
            "color": "#FF0000",
            "weight": "bold"
          }
        ],
        "cornerRadius": "5px"
      }
    ],
    "backgroundColor": "#f9f9f9"
  }
}
        line_bot_api.reply_message(event.reply_token,FlexSendMessage(alt_text="動漫通", contents=bubble3))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = 'traceback.format_exc():\n%s' % traceback.format_exc()))

def sendText3(event):  #傳送文字
    try:
        url = 'https://home.gamer.com.tw/creationCategory.php?v=1&owner=blackXblue&c=370818'
        res1 = requests.get(url).text
        
        textall = re.compile('''<tr>
<td align="left"><img src="https://i2.bahamut.com.tw/spacer.gif" class="IMG-C09" /><a href="(.+)">(.+)</a></td>
<td nowrap="nowrap"><a href="//home.gamer.com.tw/blackXblue">X洨妹</a></td>
<td nowrap="nowrap">(.+)</td>
</tr>''')
        findalltext = textall.findall(res1)
        
        # today= datetime.date.today()
        # formatted_today = today.strftime('%m/%d')
        # if formatted_today in findalltext[0][1]:
        url2 = 'https://home.gamer.com.tw/'+findalltext[0][0]
        res2 = requests.get(url2).text
        textall2 = re.compile('''<div class="MSG-list8C">&#91;(.+)&#93;<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<div><br></div><div>(.+)</div></div>''')
        findalltext2 = textall2.findall(res2)

        all_text = '{}\n{}\n{}\n{}\n{}\n{}'.format(findalltext2[0][0],findalltext2[0][2],findalltext2[0][3],findalltext2[0][4],findalltext2[0][5],findalltext2[0][6])
        text2 = [TextSendMessage(text= '{}'.format(all_text)),TextSendMessage(text = '{}'.format(findalltext2[0][7]))]
        line_bot_api.reply_message(event.reply_token,text2)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = 'traceback.format_exc():\n%s' % traceback.format_exc()))


