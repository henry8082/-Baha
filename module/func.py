from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,CarouselTemplate,URITemplateAction,CarouselColumn,FlexSendMessage

import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import datetime
import traceback
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from invoiceapi.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)


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
        
def sendText2(event):  #傳送文字
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
        #textall2 = re.compile('''<div class="MSG-list8C">&#91;(.+)&#93;<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<br>(.+)<div><br></div><div>(.+)</div></div>''')
        findalltext2 = textall2.findall(res2)
        colors = []
        for i in range(3,7):
            if  findalltext2[0][7][-1] == findalltext2[0][i][0]: colors.append(['#FF0000','bold'])
            else:colors.append(["#000000","regular"])
        
        
#         bubble2 = {
#   "type": "bubble",
#   "header": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "box",
#         "layout": "horizontal",
#         "contents": [
#           {
#             "type": "image",
#             "url": "https://p2.bahamut.com.tw/HOME/53/creation_blackxblue.PNG",
#             "size": "full",
#             "aspectMode": "cover",
#             "gravity": "center",
#             "flex": 1
#           }
#         ]
#       }
#     ],
#     "paddingAll": "0px"
#   },
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "box",
#         "layout": "vertical",
#         "contents": [
#           {
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#               {
#                 "type": "text",
#                 "size": "xl",
#                 "wrap": True,
#                 "text": findalltext2[0][0],
#                 "color": "#0000C6",
#                 "weight": "bold"
#               },
#               {
#                 "type": "text",
#                 "size": "xl",
#                 "wrap": True,
#                 "text": findalltext2[0][2],
#                 "color": "#0000C6",
#                 "weight": "bold"
#               },
#               {
#                 "type": "text",
#                 "color": "#ffffffcc",
#                 "size": "md",
#                 "contents": [
#                   {
#                     "type": "span",
#                     "text": findalltext2[0][3],
#                     "color": colors[0]
#                   }
#                 ]
#               },
#               {
#                 "type": "text",
#                 "color": "#ffffffcc",
#                 "size": "md",
#                 "contents": [
#                   {
#                     "type": "span",
#                     "text": findalltext2[0][4],
#                     "color": colors[1]
#                   }
#                 ]
#               },
#               {
#                 "type": "text",
#                 "color": "#ffffffcc",
#                 "size": "md",
#                 "contents": [
#                   {
#                     "type": "span",
#                     "text": findalltext2[0][5],
#                     "color": colors[2]
#                   }
#                 ]
#               },
#               {
#                 "type": "text",
#                 "color": "#ffffffcc",
#                 "size": "md",
#                 "contents": [
#                   {
#                     "type": "span",
#                     "text": findalltext2[0][6],
#                     "color": colors[3]
#                   }
#                 ]
#               }
#             ],
#             "spacing": "sm"
#           },
#           {
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#               {
#                 "type": "box",
#                 "layout": "vertical",
#                 "contents": [
#                   {
#                     "type": "text",
#                     "size": "xxl",
#                     "wrap": True,
#                     "margin": "lg",
#                     "color": "#FF0000",
#                     "text": findalltext2[0][7],
#                     "weight": "bold"
#                   }
#                 ]
#               }
#             ],
#             "paddingAll": "13px",
#             "backgroundColor": "#ffffff1A",
#             "cornerRadius": "2px",
#             "margin": "xl"
#           }
#         ]
#       }
#     ],
#     "paddingAll": "20px",
#     "backgroundColor": "#F0DAD2"
#   }
# }  

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

def sendText4(event):  #傳送linetoday
    def parse_source(url):
        #driver = webdriver.Chrome(r"C:\Users\user\Desktop\聯成助教資料\練習\chromedriver")
        driver.get(url)
        soup =  BeautifulSoup(driver.page_source, 'lxml')
        hrefs = soup.find_all('a','lnk vLink')
        for href in hrefs:
            #print(href['href'],'\n')
            yield parse_detail(href['href'])
    def parse_detail(url):
        driver.get(url)
        res = BeautifulSoup(driver.page_source, 'lxml')
        short_url = res.find('meta',property="og:url")['content'].split("-")[-1]
        href = "https://today.line.me/TW/pc/article/{}?utm_source=copyshare".format(short_url)
        title = res.find('meta',property="og:title")['content'].replace('【TODAY 看世界】','').replace('TODAY 看世界 | ','')
        # resq = requests.get('https://today.line.me/tw/article/%E7%A2%BA%E8%A8%BA%E6%95%B8%E9%AB%98%E5%B1%85%E5%85%A8%E7%90%83%E7%AC%AC5+%E6%AD%BB%E4%BA%A1%E7%8E%87%E5%8D%BB%E5%83%851+%E5%BE%B7%E5%9C%8B%E7%9A%84%E4%BD%9C%E6%B3%95%E7%9C%9F%E8%83%BD%E6%9C%89%E6%95%88%E9%98%B2%E7%96%AB%E5%97%8E%EF%BC%9F-1Ego09') #測試用requests的方式是否可以成功
        # res = bs(resq.text)
        time = res.find('dd','date').text.replace('發布時間 ','')
        time = datetime.datetime.strptime(time, '%Y年%m月%d日%H:%M')
        text1 = res.find('article','bx-dsc').text.strip()+'\n'+res.find('article','bx-dsc').find_all('p')[1].text.replace(u'\u3000',u'')
        article = text1.split("《TODAY 看世界》")[0]
        return {"href":href,"title":title,"time":time,"article":article}   
    
    try:
        url = 'https://today.line.me/TW/publisher/101508'
        df4 = pandas.DataFrame(list(parse_source('https://today.line.me/TW/publisher/101508')))
        all_text = '{}\n{}\n{}\n{}\n{}\n{}'.format(findalltext2[0][0],findalltext2[0][2],findalltext2[0][3],findalltext2[0][4],findalltext2[0][5],findalltext2[0][6])
        text2 = [TextSendMessage(text= '{}'.format(all_text)),TextSendMessage(text = '{}'.format(findalltext2[0][7]))]
        line_bot_api.reply_message(event.reply_token,text2)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = 'traceback.format_exc():\n%s' % traceback.format_exc()))



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
