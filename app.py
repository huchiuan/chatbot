
from linebot.models import *
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import requests 
import re

import apiai
import json
import requests
import random

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('tv8NY9n0JPLCVi6tG5DMcVz/P+cLRap9p8r6ZXsgEnB00z0rKNI+eucjsUGdaGdqri7rNtZ5SepXpyn3UZf/4x5pLd7fY+9oCwEWbPjg9tWpa6lOHBC/ZJtEIlnk9HtGJZotOcNTLA0l8bVaPzBJNAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3f27a40ad929aaf918dc9f7912d69457')
GOOGLE_API_KEY = os.environ.get('AIzaSyDwDZDXjeZJcmfmOKTyg7ytXgVte1w3Jhc')
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

      soup = BeautifulSoup(r.text, 'html.parser')


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
    # 獲取使用者的經緯度
    lat = event.message.latitude
    long = event.message.longitude

    # 使用 Google API Start =========
    # 1. 搜尋附近餐廳
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(GOOGLE_API_KEY, lat, long)
    nearby_results = requests.get(nearby_url)
    # 2. 得到最近的20間餐廳
    nearby_restaurants_dict = nearby_results.json()
    top20_restaurants = nearby_restaurants_dict["results"]
    ## CUSTOMe choose rate >= 4
    res_num = (len(top20_restaurants)) ##20
    above4=[]
    for i in range(res_num):
        try:
            if top20_restaurants[i]['rating'] > 3.9:
                #print('rate: ', top20_restaurants[i]['rating'])
                above4.append(i)
        except:
            KeyError
    if len(above4) < 0:
        print('no 4 start resturant found')
    # 3. 隨機選擇一間餐廳
        restaurant = random.choice(top20_restaurants)
    restaurant = top20_restaurants[random.choice(above4)]
    # 4. 檢查餐廳有沒有照片，有的話會顯示
    if restaurant.get("photos") is None:
        thumbnail_image_url = None
    else:
        # 根據文件，最多只會有一張照片
        photo_reference = restaurant["photos"][0]["photo_reference"]
        thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=1024".format(GOOGLE_API_KEY, photo_reference)
    # 5. 組裝餐廳詳細資訊
    rating = "無" if restaurant.get("rating") is None else restaurant["rating"]
    address = "沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
    details = "南瓜評分：{}\n南瓜地址：{}".format(rating, address)

    # 6. 取得餐廳的 Google map 網址
    map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
        lat=restaurant["geometry"]["location"]["lat"],
        long=restaurant["geometry"]["location"]["lng"],
        place_id=restaurant["place_id"]
    )
    # 使用 Google API End =========

    # 回覆使用 Buttons Template
    buttons_template_message = TemplateSendMessage(
    alt_text=restaurant["name"],
    template=ButtonsTemplate(
            thumbnail_image_url=thumbnail_image_url,
            title=restaurant["name"],
            text=details,
            actions=[
                URITemplateAction(
                    label='查看南瓜地圖',
                    uri=map_url
                ),
            ]
        )
    )


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
