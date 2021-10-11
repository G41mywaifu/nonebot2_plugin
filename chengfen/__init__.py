from .vtb import vtb
from loguru import logger
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.adapters.cqhttp import Message
import requests
global false, null, true
false = null = true = ''
chengfen=on_command('查成分')

@chengfen.handle()
async def chengfen(bot: Bot, event: Event):
    print(len(vtb))
    global false, null, true
    false = null = true = ''
    try:
        mid=str(event.message).split('查成分')[0]
        url="https://account.bilibili.com/api/member/getCardByMid?mid={}".format(mid)
        res = requests.get(url)
        attlist = eval(res.text)
        mid=attlist['card']['mid']
        name=attlist['card']['name']
        faces=attlist['card']['face']
        
        face=f'[CQ:image,file={faces}]'
        msg=""
        attlist=attlist['card']['attentions']
        a=0
        for ids in attlist:
            for i in vtb:
                
                
                if str(ids) == i['accounts'][0]['id']:
                    
                    ww=i['name']['default']
                    msg+=i['name'][ww]+', '
                    a+=1
        await bot.send(event, Message.template('{n1}(uid{n5}){n2}关注的vtb有{n3}个:{n4}').format(n1=f'{name}',n2=f'{face}',n3=f'{a}',n4=f'{msg}',n5=f'{mid}'))
        
    except:
        await bot.send(event,'出错了，可能输入的id有误')
   