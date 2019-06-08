
from linebot.models import *
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json

import requests 
import re
import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('tv8NY9n0JPLCVi6tG5DMcVz/P+cLRap9p8r6ZXsgEnB00z0rKNI+eucjsUGdaGdqri7rNtZ5SepXpyn3UZf/4x5pLd7fY+9oCwEWbPjg9tWpa6lOHBC/ZJtEIlnk9HtGJZotOcNTLA0l8bVaPzBJNAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3f27a40ad929aaf918dc9f7912d69457')

#test



# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息

def news():
    # 下載 Yahoo 首頁內容
    r = requests.get('https://tw.yahoo.com/')
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
    # 以 BeautifulSoup 解析 HTML 程式碼
      soup = BeautifulSoup(r.text, 'html.parser')

    # 以 CSS 的 class 抓出各類頭條新聞
      stories = soup.find_all('a', class_='story-title')
      content=""

      for s in stories[:5]:
        title=s.text
        href=s.get('href')
        content += '{}\n{}\n'.format(title, href)
    return content
def dcard():
    url = 'https://www.dcard.tw/f'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')
    dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
    dcard_url = soup.find_all('a', re.compile('PostEntry_root_'))

    test = []
    finalanswer = ''

    for index, item in enumerate(dcard_title[:10]):
        newurl = dcard_url[index].get('href')
        finalur = newurl.split("-")
        answer = (str)(item.text.strip()) + '\n'+"https://www.dcard.tw" + (str)(finalur[0]) + '\n\n'
        test.append(answer)
        number = (str)(index + 1) + '.'
        print(number)
        finalanswer += number
        finalanswer += test[index]
        print(index + 1, item.text.strip(), "網址:", "https://www.dcard.tw" + finalur[0])

    return finalanswer

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg=event.message.text
    msg=msg.encode('utf-8')

    if event.message.text == "新北":
        print("文字get")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='要食衣住行育樂?'))
        if event.message.text == "食":
            print("文字get")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='想吃什麼?'))
            if event.message.text == "燒烤":
                print("文字get")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='推薦給你:就醬子烤霸'))



    elif event.message.text == "定位":
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='是否要修改定位?',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    URITemplateAction(
                        label='location',
                        uri='line://nv/location'
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "子瑜抽":
       
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i.imgur.com/nVMlh8I.jpg', preview_image_url='https://i.imgur.com/nVMlh8I.jpg'))
    elif event.message.text == "新抽":
        message={
            "type": "flex",
            "altText": "Flex Message",
            "contents": {
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://tgifridays.com.tw/images/storeimages/XinYi.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "TGI FRIDAYS 星期五美式餐廳 西門餐廳",
                                    "size": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "4.0",
                                            "flex": 0,
                                            "margin": "md",
                                            "size": "sm",
                                            "color": "#999999"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "地址",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "108台北市萬華區武昌街二段72號",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                                                    "text": "營業時間",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "align": "start",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "11:30–00:00",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                            "flex": 0,
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "訂位",
                                        "uri": "https://inline.app/booking/-KzvYo7DTgcAy5Kb4khD"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "更多資訊",
                                        "uri": "https://tgifridays.com.tw/"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "spacer",
                                    "size": "sm"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://img.yukiblog.tw/img/8397c736afde_2DCA/DSCF4363.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Guru House",
                                    "size": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "4.0",
                                            "flex": 0,
                                            "margin": "md",
                                            "size": "sm",
                                            "color": "#999999"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "地址",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "108台北市萬華區武昌街二段72號",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                                                    "text": "營業時間",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "align": "start",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "10:00–00:00",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                            "flex": 0,
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "更多資訊",
                                        "uri": "https://www.facebook.com/guruhouse.ximen/"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "spacer",
                                    "size": "sm"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://img.yukiblog.tw/img/8397c736afde_2DCA/DSCF4363.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Guru House",
                                    "size": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "4.0",
                                            "flex": 0,
                                            "margin": "md",
                                            "size": "sm",
                                            "color": "#999999"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "地址",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "108台北市萬華區武昌街二段72號",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                                                    "text": "營業時間",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "align": "start",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "10:00–00:00",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                            "flex": 0,
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "訂位",
                                        "uri": "https://linecorp.com"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "更多資訊",
                                        "uri": "https://linecorp.com"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "spacer",
                                    "size": "sm"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://scontent.ftpe8-1.fna.fbcdn.net/v/t31.0-8/19620220_1569720276392036_5428174535650221833_o.jpg?_nc_cat=109&_nc_ht=scontent.ftpe8-1.fna&oh=7bfe73c6c42a0643e702ffa36a1647bc&oe=5D8777A1",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "三角三韓國道地烤肉-西門店",
                                    "size": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "4.0",
                                            "flex": 0,
                                            "margin": "md",
                                            "size": "sm",
                                            "color": "#999999"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "地址",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "108台北市萬華區漢口街二段92號",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                                                    "text": "營業時間",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "align": "start",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "17:00–23:00",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                            "flex": 0,
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "更多資訊",
                                        "uri": "https://www.facebook.com/EvilPigRestaurant/"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "spacer",
                                    "size": "sm"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://www.dookki.com.tw/首頁輪播圖//_imagecache/homepage.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "『 兩餐 』 두끼 韓國年糕火鍋吃到飽-台灣首店西門店",
                                    "size": "xl",
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "icon",
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                            "size": "sm"
                                        },
                                        {
                                            "type": "text",
                                            "text": "4.0",
                                            "flex": 0,
                                            "margin": "md",
                                            "size": "sm",
                                            "color": "#999999"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "地址",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "108台北市萬華區西寧南路123號",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                                                    "text": "營業時間",
                                                    "flex": 2,
                                                    "size": "sm",
                                                    "align": "start",
                                                    "color": "#AAAAAA"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "11:00–22:00",
                                                    "flex": 5,
                                                    "size": "sm",
                                                    "color": "#666666",
                                                    "wrap": true
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
                            "flex": 0,
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "更多資訊",
                                        "uri": "https://www.dookki.com.tw/"
                                    },
                                    "height": "sm",
                                    "style": "link"
                                },
                                {
                                    "type": "spacer",
                                    "size": "sm"
                                }
                            ]
                        }
                    }
                ]
            }
        }

        # 傳送訊息
        line.reply_message(reply_token, message)

    elif event.message.text == "新聞":
        a=news()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Yahoo前五大新聞:'+'\n'+a))

    elif event.message.text == "dcard":
        a = dcard()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Dcard十大熱門文章:' + '\n' + a))
    elif event.message.text == "測試用":
        bubble = BubbleContainer(body=BoxComponent(layout='vertical', contents=[
            TextComponent(text='請問需要什麼服務?'),
            ButtonComponent(action=MessageAction(label='請推薦餐廳', text='請推薦餐廳'))
        ]))

        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="Flex message", contents=bubble))

    elif event.message.text == "測試用2":
        Carousel = CarouselContainer(body=BoxComponent(layout='vertical',
          contents=[
            TextComponent(text='更新位置?'),
            ButtonComponent(action=URIAction(label='請給予位置', uri='line://nv/location'))
        ]))

        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="Flex message", contents=Carousel))


    else :
         message = TextSendMessage(text=event.message.text)
         line_bot_api.reply_message(event.reply_token, message)



@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    newcoming_text = "接收到位置囉"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
