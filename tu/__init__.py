from nonebot import get_bot
import asyncio
from datetime import datetime
import os
import random
from nonebot.permission import SUPERUSER
from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.adapters.cqhttp.utils import escape
from aip import AipContentCensor
from nonebot.plugin import on_message,on_command
from src.util import FreqLimiter
import re
import shutil
from nonebot.permission import SUPERUSER
global_config = get_driver().config
global path,file_dir,file_list,path2,whitepath
whitepath="C:\\mirai\\data\\images\\white"
path="C:\\mirai\\data\\images"
path2="C:\\mirai\\data\\images\\block"
file_dir ='C:\mirai\data\images'
file_list = os.listdir(file_dir)
lmt = FreqLimiter(10)
getimg=on_command('图库')
delimg=on_command('del',permission=SUPERUSER,priority=1,block=True)
setu=on_message(priority=6)
helptu=on_command('偷图帮助')
cache = 'C:\\mirai/'  #你go-cqhttp.exe的文件夹
APP_ID = '' #你的AppID
API_KEY = ''#你的API Key
SECRET_KEY = ''#你的Secret Key
client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def porn_pic_index(img):
    img = os.path.join(cache,img)
    result = client.imageCensorUserDefined(get_file_content(img))
    try:
        if (result):
            r = result
            if "error_code" in r:
                return { 'code': r['error_code'], 'msg': r['error_msg'] }
            else:
                porn = 0
                sexy = 0
                for c in r['data']:
                   
                    if c['type'] == 1 and c['subType'] == 0:
                        porn = int(c['probability'] * 500)
                    elif c['type'] == 1 and c['subType'] == 1:
                        sexy = int(c['probability'] * 500)
                return { 'code': 0, 'msg': 'Success', 'value': max(sexy,porn) }

        else:
            return { 'code': -1, 'msg': 'API Error' }


    except FileNotFoundError:
        return { 'code': -1, 'msg': 'File not found' }



def saveimg(file_dir,file,aim):
    file_list = os.listdir(file_dir)
    for image in file_list:
        if image == file:
                if os.path.exists(os.path.join(file_dir,aim)):
                    shutil.copy(os.path.join(file_dir,image), os.path.join(file_dir, aim))
                else:
                    os.makedirs(os.path.join(file_dir,aim))
                    shutil.copy(os.path.join(file_dir, image), os.path.join(file_dir, aim))    




@setu.handle()
async def on_input_chara_name(bot, event:GroupMessageEvent):
    if 'del' in str(event.message):
        return
    global path,file_dir,file_list,whitepath
    flag=False
    for msg in event.message:
        if msg.type=="image":
            
            ret = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(msg))
   
            try:
                file = ret.group(1)
            except:
                await bot.send(event,'呜呜呜')
                return    
            img = await get_bot().get_image(file=file)  

            for x in os.listdir(path2):
                if x==file:
                    
                    return
            for x in os.listdir(whitepath):
                if x==file:
                    return
            
        
            img_file = img['file']
            porn = porn_pic_index(img_file)
            if porn['code'] == 0:
                score = porn['value']
            else:
                code = porn['code']
                err = porn['msg']
                await bot.send(event,f'错误:{code}\n{err}')
                return
            url = os.path.join(cache,img_file)
           
            if score>4:               
                saveimg(path,file,'white')
                
                flag=True
    if flag==True and  lmt.check(event.user_id) and score>30:
        await bot.send(event,"好图 偷了")
        lmt.start_cd(event.user_id)
           
@getimg.handle()
async def Entity(bot, event):
    global path,file_dir,file_list,whitepath
    
    imgs = []
    for x in os.listdir(whitepath):
        if x.endswith('image'):
            imgs.append(x)
    if len(imgs)==0:
        await getimg.send('图库为空')
        return
    selected_imgs=random.sample(imgs,1)
    for i in selected_imgs:
       
        img = await get_bot().get_image(file=i)
        img_file = img['file']
        
        url = os.path.join(cache,img_file)
        msgs=MessageSegment.image(f'file:///{os.path.abspath(url)}')
        await bot.send(event,msgs)
        
@delimg.handle()
async def on_input_chara_name(bot, event):
    
    global path,file_dir,file_list,whitepath
    flag=False
    for msg in event.message:
        if msg.type=="image":
            
            ret = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(msg))
   
            try:
                file = ret.group(1)
            except:
                await bot.send(event,'呜呜呜')
                return
     
            img = await get_bot().get_image(file=file)
            
            img_file = img['file']
           
            saveimg(path,file,'block')
    
    file_name = whitepath+'//'+file
    if os.path.exists(file_name):
        os.remove(file_name)
        
        await bot.send(event,"成功删除")
    else:
        
        await bot.send(event,"删除失败  文件可能未存在")

@helptu.handle()
async def helptu(bot,event):
    msg="有人发送图片将自动使用 API进行打分 大于一定分数将自动保存\n发送 图库 随机提取一张\n发送del+图片 删除已保存的图片 并加入黑名单"
    await bot.send(event,msg)
