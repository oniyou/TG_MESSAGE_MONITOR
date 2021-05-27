#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @178，原作者不知道，修改自1.py
"""
运行环境为python3,运行前先输入python -V(大写V)看看python版本，如果是python 2.x.x就没得玩，去安装python3
脚本自动安装依赖，如果安装失败请手动pip3 install telethon pysocks httpx 或者 py -3 -m pip install telethon pysocks httpx，或者pip换源后再安装
如果运行失败或者依赖安装不成功先python -V(大写V)看看python版本是否为python3,然后再输入pip -V(大写V)看看版本是不是21.x.x，然后最后面跟着的是不是python3.x.x

使用方法：
1.填好20、21、23三行变量，如无必要，请别动其他地方
2.使用python /脚本绝对路径/178.py运行脚本，输入手机号登录，记得加区号，比如中国号码就是+8617811112222，然后输入tg发的验证码
3.提示登录成功就ok了

测试方法：
1.复制(https://api.m.jd.com)，带上括号，发送到Telegram，就是发送验证码那个Telegram，或者复制频道里一键领取的信息发送到Telegram
2.正常会打印"【xxxx;】xxx"，如果ck有问题可以取消121行注释查看ck，取消注释请对齐代码，否则会报错
"""
import os
# ========================下面要改===========================
# 前两个变量请打开https://my.telegram.org，在API development tools里面获取
api_id = '4506196'
api_hash = '093bcb219a7f2fe605fe083ae7decbb7'
# cookie，多个cookie请用&隔开，如pt_key=111;pt_pin=111;&pt_key=222;pt_pin=222;
cookies = os.environ["JD_COOKIE"]
# ↑↑↑↑↑↑↑↑以上为必填项↑↑↑↑↑↑↑↑

# ↓↓↓↓↓↓↓↓以下为选填项↓↓↓↓↓↓↓↓
push_switch = False # 默认关闭推送，如需启用代理请改为True
tg_proxyswitch = False # 默认关闭代理，如需启用代理请改为True
tg_proxy = {
    'proxy_type': 'socks5', # （必选）协议，可用协议：socks5、socks4、http
    'addr': '1.1.1.1',      # （必选）ip
    'port': 5555,           # （必选）端口号
    # 'username': 'foo',      # （可选）用户名
    # 'password': 'bar',      # （可选）密码
    # 'rdns': True            # （可选）使用远程解析还是本地解析，默认远程
}
bot_token = ''# 机器人token
user_id = ''# tgid
# ========================上面要改===========================

print('脚本版本：v0.4')
print('低调使用，请不要传播旧版！！！也不要往群里发信息！！！\n'*3)
print('如果依赖安装失败请手动安装，或者pip换源之后再安装.报错尝试注释168行')

count = 3
while count:
    try:
        pip_v = ''.join(os.popen('pip -V'))
        v = ''.join(pip_v.split(' ', 2)[1]).split('.',1)
        if int(v[0]) < 21:
            print('正在更新pip')
            try:
                os.system('python -m pip install --upgrade pip')
            except:
                print('pip更新失败，请手动更新python -m pip install --upgrade pip')
        break
    except:
        if count != 3:
            print('安装pip失败，正在重新安装,如果没有wget请手动安装wget')
        print('开始安装pip')
        os.system('wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate && python get-pip.py')
        count -= 1
        continue
count = 3
while count:
    try:
        from telethon import TelegramClient, events, sync        
        break
    except:
        if count != 3:
            print('安装telethon失败，正在重新安装')
        print('开始安装telethon')
        os.system('pip install telethon')
        count -= 1
        continue
count = 3
while count:
    try:
        import httpx
        break
    except:
        if count != 3:
            print('安装httpx失败，正在重新安装')
        print('开始安装httpx')
        os.system('pip install httpx')
        count -= 1
        continue

import time,json,re,asyncio

if tg_proxyswitch:
    client = TelegramClient('Telethon', api_id, api_hash, proxy=tg_proxy)
else:
    client = TelegramClient('Telethon', api_id, api_hash)

try:
    client.start()
except:
    if tg_proxyswitch:
        print('登录失败，正在安装pysocks')
        print('虽然不一定有用，但装了再说')
        print('默认使用清华源，国外机速度过慢可以手动安装：pip install pysocks，或者修改脚本97行')
        os.system('python -m pip install pysocks -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com')# 使用默认源请将引号里的内容修改为pip install pysocks
        try:
            client.start()
        except:
            print('登录失败，可能是pysocks没有正确安装，或者后台已运行此脚本')
            os._exit(0)# 删掉括号里的0可查看报错消息
    else:
        print('登录失败，虽然不知道发生了什么，但请检查后台是否已运行此脚本，也许可以试试重启，万一呢？')
        os._exit(0)# 删掉括号里的0可查看报错消息

tg_url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=' % (bot_token,user_id)

async def send_live(cookies, url):
    if len(cookies) > 0:
        giftDesc = ['关注有礼\n']
        str_ck = cookies.split('&')
        for i in range(1, len(str_ck) + 1):
            if len(str_ck[i - 1]) > 0:
                # print(str_ck[i-1])# ck有问题的请取消注释这一行，查看输出的ck对不对
                header = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
                    "Cookie": str_ck[i - 1],
                }
                async with httpx.AsyncClient() as client:
                    r = await client.get(url=url, headers=header)
                    r1 = json.loads(r.text)
                    pin = str_ck[i - 1].split('=')
                    if "result" in r1:
                        if "alreadyReceivedGifts" in r1["result"]:
                            if push_switch:
                                g = ''
                                for x in r1["result"]["alreadyReceivedGifts"]:
                                    g += ('[' + x["redWord"] + x["rearWord"] + x["secLineWord"] + ']    ')
                                giftDesc.append('【' + pin[2] + '】' + g)
                            print('【' + pin[2] + '】' + g)
                        elif "followResult" in r1["result"] and r1["result"]["followResult"] != True:
                            if push_switch:
                                giftDesc.append('【' + pin[2] + '】' + '店铺未取关')
                            print('【' + pin[2] + '】' + '店铺未取关')
                        elif "giftResult" in r1["result"] and r1["result"]["giftResult"] != True:
                            if push_switch:
                                giftDesc.append('【' + pin[2] + '】' + '未领取到，可能是领取CD没好')
                            print('【' + pin[2] + '】' + '未领取到，可能是领取CD没好')
                    elif "message" in r1:
                        if push_switch:
                            giftDesc.append('【' + pin[2] + '】' + 'cookie无效')
                        print('【' + pin[2] + '】' + 'cookie无效')
                    elif "echo" in r1:
                        if push_switch:
                            giftDesc.append('【' + pin[2] + '】' + '拒绝')
                        print('【' + pin[2] + '】' + '拒绝')
                    else:
                        if push_switch:
                            giftDesc.append('【' + pin[2] + '】' + '未知错误' + str(r1))
                        print('【' + pin[2] + '】' + '未知错误' + str(r1))
                await asyncio.sleep(0.5)
    text = '\n'.join(giftDesc)
    httpx.get(tg_url + text)

async def main():
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

p1 = re.compile(r'[(](https://api\.m\.jd\.com.*?)[)]', re.S)

client.send_message('Telegram', '测试消息往这里发')# 报错尝试注释这行
@client.on(events.NewMessage(chats=[-1001197524983]))# 布道场频道
@client.on(events.NewMessage(chats=[777000]))# Telegram，测试用

async def my_event_handler(event):
        print(event.message.sender_id,event.message.text)
        print('上面是你的加入的频道、群组、联系人名称及id')
        print('登录成功，正在监控频道及Telegram')
        sec = re.findall(p1, event.message.text)
        if sec!=[]:
            await send_live(cookies,sec[0])

with client:
    client.loop.run_until_complete(main())
    client.loop.run_forever()
