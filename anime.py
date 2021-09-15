import re
import json
import requests
import datetime
from io import BytesIO
from PIL import Image

from src.Service import Service
from src.util import pic2b64, FreqLimiter
from src import R
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent,
                                           MessageEvent, PrivateMessageEvent)
sv = Service('traceanime')

enable_details = True #是否返回详细信息，启用此项查询速度会变慢
minsim = 0.70 #匹配度，0.90以下的可能会不太准

query = '''
query ($id: Int) {
  Media (id:$id) {
    coverImage {
        large
    }
    startDate {
        year
        month
        day
    }
    endDate {
        year
        month
        day
    }
    season
    seasonYear
    type
    format
    status
    episodes
  }
}
'''

def get_pic(address):
    return requests.get(address,timeout=20).content

def get_details(anilist_id):
    variables = {
        'id': anilist_id
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    print(response.content)
    dic = json.loads(str(response.content,'utf-8'))
    return dic['data']['Media']

@sv.on_startswith(('搜番', '查番', '找番', '识番'))
async def traceanime(bot, event: Event):
    text=str(event.message)
    text=f"[{text.split('[')[1]}"
    print(text)
    print(text)
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(text))
    pic_url = ret.group(2)
    url = f'https://api.trace.moe/search?anilistInfo&cutBorders&url={pic_url}'
    try:
        with requests.get(url, timeout=20) as resp:
            res = resp.json()
            data = res['result'][0]
            print(data)
            similarity = "%.2f%%" % (data['similarity'] * 100)
            episode = data['episode']
            from_time = datetime.timedelta(seconds=data['from'])
            to_time = datetime.timedelta(seconds=data['to'])
            anilist = data['anilist']
            title_native = anilist['title']['native']
            title_romaji = anilist['title']['romaji']
            title_english = anilist['title']['english']
            video = data['video']

            is_adult = '分级：普通'

            if anilist['isAdult']:
                is_adult = '分级：限制级'
            if data['similarity'] < minsim:
                msg = '相似度'+similarity+'过低，可能原因：图片为局部图/图片清晰度太低...'
            else:
                details_str = ''
                if enable_details:
                    details = get_details(anilist['id'])
                    print(details)
                    #过滤里番封面
                    if anilist['isAdult']:
                        image = ''
                    else:
                        image=''
                        image1 = MessageSegment.image(pic2b64(Image.open(BytesIO(get_pic(details['coverImage']['large'].replace('\\',''))))))

                    types = details['type']
                    formats = details['format']
                    ep_num = details['episodes']
                    start = str(details['startDate']['year'])+'-'+str(details['startDate']['month'])+'-'+str(details['startDate']['day'])
                    if details['status'] == 'FINISHED':
                        end = str(details['endDate']['year'])+'-'+str(details['endDate']['month'])+'-'+str(details['endDate']['day'])
                    else:
                        end = '未完结'
                    details_str = f'{image}\n类型：{types}-{formats}，共{ep_num}集\n开播：{start}\n完结：{end}\n'
                if type(episode) is int:
                    msg = f'[{similarity}]该截图出自第{episode}集{from_time}至{to_time}\n{title_native}\n{title_romaji}\n{title_english}\n{details_str}{is_adult}'
                else:
                    msg = f'[{similarity}]该截图出自{episode}{from_time}至{to_time}\n{title_native}\n{title_romaji}\n{title_english}\n{details_str}{is_adult}'
            
            
            await bot.send(event, msg+'\n视频预览：' + video + '\n低于90%的结果可能会不太准确(可能原因：图片为局部图/图片清晰度太低)\n')
    except Exception as ex:
        print(ex)
        await bot.send(event, '查询错误，请稍后重试...')
