网页截图  
没有在LINUX中测试过  
安装依赖selenium  
在服务器中安装chrome浏览器和chromedriver，需要相同版本  
将14行的chromedriver改为你的chromedriver的路径  
45行C:\nb2\mimibot\src\plugins\pcr-rank\img\imgs中的C:\nb2\mimibot\src\plugins\pcr-rank\img改为你RES_DIR的路径  
效果如图   
![图片](https://user-images.githubusercontent.com/81564864/134751761-2df7eb04-efa0-4327-8cba-4f6cb593e968.png)  

查成分 这个b到底关注了多少V  
查成分+b站uid  
 ![图片](https://user-images.githubusercontent.com/81564864/136749812-00f0c282-735a-4926-a711-71af59096ebe.png)
数据来源 vtbs.moe  


偷图  
当检测到有图片发出  将对图片进行打分  并存到指定文件夹  发送  图库 随机提取一张图片  发送del+已有图片  删除此图并拉黑

修改部分hoshino的插件，使他能在nonebot2中运行  
将py文件夹下的文件放于src路径下  
改的很烂，能用就行  

项目原地址：  
5k：https://github.com/pcrbot/5000choyen  
无中生友 搜番：https://github.com/pcrbot/cappuccilo_plugins    
塔罗牌：https://github.com/haha114514/tarot_hoshino  
rank表：https://github.com/pcrbot/pcr-rank  
在env文件中加入  
RES_DIR=""  
CACHE_DIR=""  
如  
RES_DIR="C:\Resources/"  
CACHE_DIR="C:\cache/"  
在RES_DIR文件夹中创建img文件夹，将card中的asset文件夹放入img中  

