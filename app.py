
from linebot.models import *
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests 

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
def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h1 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg=event.message.text
    msg=msg.encode('utf-8')
    if event.message.text == "文字":
        print("文字get")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    elif event.message.text == "貼圖":
        print("貼圖get")
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=1,sticker_id=2))
    elif event.message.text == "圖片":
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='圖片網址', preview_image_url='圖片網址'))
    elif event.message.text == "最新電影":
     
        a=movie()
        print(a +" 55555555555")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a.text))
    elif event.message.text == "新聞":
     
        a=news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Yahoo前五大新聞'))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
    else :
         message = TextSendMessage(text=event.message.text)
         line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
