#-*- coding:utf-8 -*-
# @Author  : lx

import aiohttp
import asyncio
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
url = 'https://www.baidu.com'
async def fetch(url,proxies=None,method="get"):
    async with aiohttp.ClientSession() as session:
        if method == "get":
            async with session.get(url=url,headers=headers,proxy=proxies) as resposne:
                return await resposne.text()
        elif method == "post":
            async with session.post(url=url,headers=headers, data={},proxy=proxies) as resposne:
                return await resposne.text()
        else:
            raise ("request method error")
def callback(task):
    print('This is callback')
    # 获取响应数据
    page_text = task.result()
    print(page_text)
    print("接下来就可以在回调函数中实现数据解析")

loop = asyncio.get_event_loop()
cone = fetch(url)
task = asyncio.ensure_future(cone)
tasks = [task]
task.add_done_callback(callback)
loop.run_until_complete(asyncio.wait(tasks))

