import re

import json
import os
import datetime
import requests
from io import BytesIO
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from src.Service import Service
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters import Bot, Event
from src.util import pic2b64, FreqLimiter
from src import R
from nonebot.adapters.cqhttp.message import MessageSegment
sv = Service('pengyou', visible=False)

 

def get_pic(qq):
    apiPath=f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=100'
    return requests.get(apiPath,timeout=20).content

def load_config(path):
    try:
        with open(path,'r',encoding='utf8') as f:
            config = json.load(f)
            return config
    except:
        return {}

      
@sv.on_regex(r'^我的(.*)想说(.*$)')
async def friend(bot, event: GroupMessageEvent):
    
    
    data = load_config(os.path.join(os.path.dirname(__file__),'config.json'))['friend']
    arr = []
    is_at = False
    for m in event.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            arr = [int(m.data['qq'])]
            if int(m.data['qq']) == 1095186908:
                await bot.send(event,"爬")
                return
            
            is_at = True
        
    if not is_at:
        return
        
    match = event.match
    name = match[1-1]
    msg = (match[2-1].split('['))[0]
    
    if name==None or msg==None:
        return
    image = Image.open(BytesIO(get_pic(choice(arr))))
    img_origin = Image.new('RGBA', (100, 100), (255, 255, 255))
    scale = 3
    
    r = 100 * scale
    alpha_layer = Image.new('L', (r, r), 0)
    draw = ImageDraw.Draw(alpha_layer)
    draw.ellipse((0, 0, r, r), fill = 255)
    
    alpha_layer = alpha_layer.resize((100, 100), Image.ANTIALIAS)
    img_origin.paste(image, (0, 0), alpha_layer)

    
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'simhei.ttf'), 30)
    font2 = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'simhei.ttf'), 25)
   
    image_text = Image.new('RGB', (450, 150), (255, 255, 255))
    draw = ImageDraw.Draw(image_text)
    draw.text((0, 0), name, fill = (0, 0, 0), font = font)
    draw.text((0, 40), msg, fill = (125, 125, 125), font = font2)

    image_back = Image.new('RGB', (700,150), (255, 255, 255))
    image_back.paste(img_origin, (25, 25))
    image_back.paste(image_text, (150, 40))
    
    await bot.send(event, MessageSegment.image(pic2b64(image_back)))


 
@sv.on_keyword(('吃什么','吃啥'))
async def diary(bot, event):
    food=[
    '烤鸭',
    '油泼面',
    '布丁',
    '屎',
    '重庆小面',
    '酸菜鱼',
    '螺蛳粉',
    '沙拉',
    '炸酱面',
    '汉堡',
    '披萨',
    '黄焖鸡',
    '烤串',
    '寿司',
    '雪糕',
    '手抓饼',
    '麻辣香锅',
    '凉皮',
    '叫花鸡',
    '烧麦',
    '羊肉汤'
    ]
    msg=[
    '{}怎么样',
    '小建议 吃{}',
    '{}爱吃吃，不吃爬',
    '今天吃{}',
    '我命令你吃{}',
    '突然有点想吃{}',
    '吃点{}吧',
    '{}就很不错',
    '好久没吃{}了',
    '那必须是{}',
    '要不就吃{}',
    '除了{}还能是什么',
    '显然是{}',
    '{}。'
    ]
    select = choice(food)
    await bot.send(event,choice(msg).format(select)+R.img(f'food//{select}.jpg').cqcode)