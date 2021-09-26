from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options
from loguru import logger
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.plugin import on_command,on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.message import MessageSegment


pic=on_regex('^截图(.*)$')


def webshot(url,saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options,executable_path =chromedriver)
    driver.maximize_window()
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    link = url 
    try:
        driver.get(link)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(picname + ".png")
        
        return True
    except Exception as e:
        return False
       
       
@pic.handle()
async def pic(bot: Bot, event: Event, state: T_State):
    path=state["_matched_groups"]
    path=path[0]
    if 'http://' not in path and 'https://' not in path:
        path='http://'+path
    ss=webshot(path,'C:\\nb2\\mimibot\\src\\plugins\\pcr-rank\\img\\imgs')
    if ss==True:
        
        await bot.send(event, MessageSegment.image('file:///C:\\nb2\\mimibot\\src\\plugins\\pcr-rank\\img\\imgs.png'))
    else:
        await bot.send(event,'获取失败 呜呜呜')
    
