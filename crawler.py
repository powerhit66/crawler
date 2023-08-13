# coding: utf-8
import scrapy
from .csv_write import csv_write
import logging
import os
import requests

# 定数
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAA8SdNPXw/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=kVBG0SLOoUAAQvzosalSPehThP5q2RGIFGeQgM1xZ90%3D"
ANSWER_URL = "https://chat.googleapis.com/v1/spaces/AAAA8SdNPXw/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=YEe_Zu3CYsnmsFdRhnqvUMFaxgUZPeqJStcO40255hQ%3D"


output = {}

class FeCrawl(scrapy.Spider):
    name = "fe_crawl"
    allowed_domains = ["ap-siken.com", ""]
    start_urls = ["https://www.ap-siken.com/apkakomon.php"]


    def parse(self, response):
       return scrapy.FormRequest.from_response(
            response,
            formdata={},
            callback=self.print
        )

    def print(self, response):
       options = ["a", 'i', 'u', 'e']

       base = "https://www.ap-siken.com/"

       while True:
           # 質問エレメント取得
           question = response.css("div.main.kako.doujou div::text").get()

           # 質問Img取得
           question_img =  response.css("div.main.kako.doujou div.img_margin img::attr(src)").get()

           # 選択肢リスト作成
           option_list = [response.css(f"span#select_{a}::text").get() for a in options]
           if option_list[0] is None:
               continue
        

           # 選択肢に画像がある場合、取得
           option_img_list = []
           request_options_img_src = [response.css(f"span#select_{a} img::attr(src)").get() for a in options]
           if request_options_img_src[0] is not None:
               option_img_list = ["https://www.ap-siken.com" + a.replace(".", ",", 1) for a in option_img_list]

           # 解答
           answer= response.css("div.ansbg.R3tfxFm5::text").get()

           # 解答の画像
           answer_img = response.css("div.ansbg.R3tfxFm5 div.img_margin img::attr(src)").get()

           #print(question)
           #print(option_list)
           #print(answer)
           #print(answer_img)
           print(option_img_list)

           options = ""
           for index, option in enumerate(option_list):

               options = f"{options}{str(index+1)}. {option}\n"

           print(options)


           title = 'こんにちは'
           subtitle = '出題です。'
           paragraph = 'これは通知ですよね。'
           question = {'textParagraph': {'text': question}}
           options = {'textParagraph': {'text': options}}


           if question_img is not None:
               question_img = "https://www.ap-siken.com" + question_img.replace("." ,"", 1)

           print(question_img)

           image = {'image': {'imageUrl': question_img, 
                            "onClick": {
                    "openLink": {
                        "url": question_img,
                    }
                    },'altText': "image"}}

           res = requests.post(
               ANSWER_URL,
               json={
                   'cards': [
                       {
                           'header': {
                               'title': title,
                               'subtitle': subtitle,
                           },
                           'sections': [
                               {'widgets': [question]}, 
                               {'widgets': [image]}, 
                               {'widgets': [options]}
                           ]
                       }
                   ]
               },
           )
           print(res.json())
       
           title = 'こんにちは'
           subtitle = '解答です。'
           paragraph = 'これは通知ですよね。'
           widget = {'textParagraph': {'text': answer}}
           res = requests.post(
               ANSWER_URL,
               json={
                   'cards': [
                       {
                           'header': {
                               'title': title,
                               'subtitle': subtitle,
                           },
                           'sections': [{'widgets': [widget]}],
                       }
                   ]
               },
           )
           print(res.json())

           if option_list[0] is not None:
               break