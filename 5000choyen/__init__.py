from PIL import Image
import random
from src.Service import Service 
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent,
                                           MessageEvent, PrivateMessageEvent)
from src.util import FreqLimiter, DailyNumberLimiter, pic2b64
from nonebot.adapters.cqhttp.message import MessageSegment
from .generator import genImage

lmt = DailyNumberLimiter(10)

sv = Service('5000choyen')

@sv.on_startswith(('5k','5K'))
async def gen_5000_pic(bot, event: MessageEvent):
    uid = event.user_id
    
    gid = event.group_id
    mid= event.message_id
    if not lmt.check(uid):
        await bot.send(event, f'您今天已经使用过10次生成器了，休息一下明天再来吧~', at_sender=True)
        return
    try:
        keyword = event.message.extract_plain_text().strip()
        
        if keyword[1]=='k':
            keyword=keyword.split('k')[1]
        else:
            keyword=keyword.split('K')[1]
        if not keyword:
            await bot.send(ev, '请提供要生成的句子！')
            return
        if '｜' in keyword:
            keyword=keyword.replace('｜','|')
        upper=keyword.split("|")[0]
        downer=keyword.split("|")[1]
        ##print('123')
        #print(upper,downer)
        img=genImage(word_a=upper, word_b=downer)
        
        await bot.send(event, MessageSegment.image(pic2b64(img)))
        
        lmt.increase(uid)
    except OSError:
        await bot.send(event, '生成失败……请检查字体文件设置是否正确')
    except:
        await bot.send(event, '生成失败……请检查命令格式是否正确')
