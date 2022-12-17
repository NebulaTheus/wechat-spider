import requests
import json
import csv
import time
import os

def get_token():
    os.system('adb shell input swipe 0 200  800 200')  #从屏幕左边缘右滑返回上一级
    time.sleep(0.5)
    os.system('adb shell input tap 557 1578')          #点击 【查看历史消息】 进入历史消息页面，坐标每个手机不一样
    time.sleep(2)
    os.system('adb shell input swipe 500 1800  500 300 100') #两次向上滑动触发加载更多
    os.system('adb shell input swipe 500 1800  500 300 100')
    time.sleep(0.1)
    url='http://127.0.0.1:8080'
    r=requests.get(url)   #向本地web服务器发送get请求获取appmsg_token和cookie
    d=eval(r.text)
    print('获取token：',d)
    # token = d['token']
    # cookie = d['cookie']
    return(d)

def crow(biz):
    MARK=0 #一个公众号文章是否抓完的标志位，1表示抓完
    data=get_token()
    token=data['token']
    cookie=data['cookie']
    n=0
    while MARK==0:
        time.sleep(0.5)
        pages = str(10 * n)
        url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz='+biz+'&f=json&offset=' +pages+ '&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=%2F%2FMLfYzV4VmptckJ%2BGC%2FEMbuBaYdCzplfP7pig2nHKORwHh%2FKcSp5ufJNIY4R6Y6&wxtoken=&'+token
        head = {'Host': 'mp.weixin.qq.com',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; GN8002 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044205 Mobile Safari/537.36 MicroMessenger/6.6.3.1260(0x26060339) NetType/WIFI Language/zh_CN',
                'Accept': '*/*',
                'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5NzAwMzU0MA==&scene=124&devicetype=android-23&version=26060339&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=5IruuVAhjeQ22KmpbBJX10LUhvreqP%2F4zCi0%2FlKRAYVSGufFu4EDGCytd7oIWNkV&wx_header=1',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.3&TBSVC=43603&CO=BK&COVC=044205&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= GN8002 &RL=1080*1920&OS=6.0&API=23',
                'Q-GUID': '37319016da4caf7783df5bf913b788cb',
                'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b',
                'cookie': cookie
                }
        try:
            r = requests.get(url, headers=head,timeout=5)
            html = json.loads(r.text)
            if len(html)==9:  #判断下返回的json消息体是否是正常的消息体
                datas0 = html['general_msg_list']
                datas0 = json.loads(datas0)
                datas = datas0['list']
                l = len(datas)
                if l<10:
                    MARK=1
                end=time.time()-start
                print('*********************')
                print('Page:%d' % n, 'Num:%d' % l,'Time:%d'%end)
                n += 1
                for data in datas:
                    try:
                        url_1 = data['app_msg_ext_info']['content_url']
                        title_1 = data['app_msg_ext_info']['title']
                        print(title_1)
                        print(url_1)
                        dd = data['app_msg_ext_info']['multi_app_msg_item_list']
                        #保存到本地
                        with open('weixin.csv','a',newline='',encoding='gb18030')as f:
                            write=csv.writer(f)
                            if len(dd) > 0:
                                for d in dd:
                                    url_d = d['content_url']
                                    title_d = d['title']
                                    print(title_d)
                                    print(url_d)
                                    write.writerow([title_d,url_d])
                    except Exception as e:
                        print(e)
                        print(r.text)
            else:
                #如果访问失效重新获得token、cookie
                print('error')
                print(r.text)
                data = get_token()
                token = data['token']
                cookie = data['cookie']

        except:
            pass
    print('*******************',biz,'抓取完成***************')


if __name__=='__main__':
    start=time.time()
    biz_list=['MzIxNDEzNzI4Mg==','MzA5OTA0NDIyMQ==','MTgwNTE3Mjg2MA==','MzA3MDM5ODY4Ng==','MjM5MDMyMzg2MA==','MzA4MjQxNjQzMA==','MzU2MzA2ODk3Nw==','MTI0MDU3NDYwMQ=='] #局座召忠、占豪、冷兔、美闻参阅、十点读书、新华网、新京报、央视新闻
    for biz in biz_list:
        crow(biz)
    print('This is new!')


