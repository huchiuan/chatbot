
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
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='信用卡優惠查詢', weight='bold', size='xl'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='類別',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='休閒娛樂',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # first row
                    BoxComponent(
                        layout='horizontal',
                        spacing='sm',
                        contents=[
                            # callAction, separator, websiteAction
                            SpacerComponent(size='sm'),
                            # callAction
                            ImageComponent(
                                url='https://i.imgur.com/ZvAirq6.png',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='LOVE 晶緻悠遊寵愛紅卡', text='LOVE 晶緻悠遊寵愛紅卡')
                            ),
                            # separator
                            SeparatorComponent(),
                            # websiteAction
                            ImageComponent(
                                url='https://i.imgur.com/rR6lQka.jpg',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='HappyCash & HAPPY GO 聯名卡(愛戀紅)',
                                                     text='HappyCash & HAPPY GO 聯名卡(愛戀紅)')
                            )
                        ]
                    ),
                    # second row
                    BoxComponent(
                        layout='horizontal',
                        spacing='sm',
                        contents=[
                            # callAction, separator, websiteAction
                            SpacerComponent(size='sm'),
                            # callAction
                            ImageComponent(
                                url='https://i.imgur.com/GSXzOsv.png',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='華南夢時代聯名卡', text='華南夢時代聯名卡')
                            ),
                            # separator
                            SeparatorComponent(),
                            # websiteAction
                            ImageComponent(
                                url='https://i.imgur.com/K4cAACy.jpg',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='HappyCash & HAPPY GO 聯名卡(爵愛黑)',
                                                     text='HappyCash & HAPPY GO 聯名卡(爵愛黑)')
                            )
                        ]
                    ),
                    # third row
                    BoxComponent(
                        layout='horizontal',
                        spacing='sm',
                        contents=[
                            # callAction, separator, websiteAction
                            SpacerComponent(size='sm'),
                            # callAction
                            ImageComponent(
                                url='https://i.imgur.com/6Vd175b.jpg',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='HappyCash & HAPPY GO 聯名卡(超級現金回饋)',
                                                     text='HappyCash & HAPPY GO 聯名卡(超級現金回饋)')
                            ),
                            # separator
                            SeparatorComponent(),
                            # websiteAction
                            ImageComponent(
                                url='https://i.imgur.com/oTyud1r.png',
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover',
                                action=MessageAction(label='現金回饋', text='現金回饋')
                            )
                        ]
                    ),
                ]
            ),
        )
        flex_template = FlexSendMessage(alt_text="hello", contents=bubble)

        line_bot_api.reply_message(
            event.reply_token,
            flex_template
        )


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
        carousel_template_message = TemplateSendMessage(
            alt_text='目錄 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
                        title='選擇服務',
                        text='請選擇',
                        actions=[
                            MessageAction(
                                label='開始玩',
                                text='開始玩'
                            ),
                            URIAction(
                                label='影片介紹 阿肥bot',
                                uri='https://youtu.be/1IxtWgWxtlE'
                            ),
                            URIAction(
                                label='如何建立自己的 Line Bot',
                                uri='https://github.com/twtrubiks/line-bot-tutorial'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/DrsmtKS.jpg',
                        title='選擇服務',
                        text='請選擇',
                        actions=[
                            MessageAction(
                                label='other bot',
                                text='imgur bot'
                            ),
                            MessageAction(
                                label='油價查詢',
                                text='油價查詢'
                            ),
                            URIAction(
                                label='聯絡作者',
                                uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/h4UzRit.jpg',
                        title='選擇服務',
                        text='請選擇',
                        actions=[
                            URIAction(
                                label='分享 bot',
                                uri='https://line.me/R/nv/recommendOA/@vbi2716y'
                            ),
                            URIAction(
                                label='PTT正妹網',
                                uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                            ),
                            URIAction(
                                label='youtube 程式教學分享頻道',
                                uri='https://www.youtube.com/channel/UCPhn2rCqhu0HdktsFjixahA'
                            )
                        ]
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    elif event.message.text=="新新抽":
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

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
