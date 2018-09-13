from aiohttp import web
import re
#接收anyproxy的post请求并处理
async def get(request):
    n=await request.post()
    url=n['url']
    cookie=n['cookie']
    biz=re.search('biz=.{14}==',url).group()   #从url中提取出_biz
    print(biz)
    token = re.search('appmsg_token.+json', url).group() #从url中提取出appmsg_token
    print('获取token：  ',token)
    print('获取cookie：  ',cookie)
    data={'token':token,'cookie':cookie}
    p_list.append(data)
    print('当前列表长度：',len(p_list))
    return web.Response(text='你好，收到信息')
#接收爬虫代码的get请求并返回appmsg_token和cookie
async def give(request):
    print('开始发送消息')
    d=p_list.pop()
    return web.Response(text=str(d))

p_list=[]  #用于存储appmsg_token和cookie
app=web.Application()
app.add_routes([web.post('/',get),web.get('/',give)])  #路由定义，有post请求访问127.0.0.1:8080，执行get函数，有get请求访问127.0.0.1:8080，执行give函数
web.run_app(app,host='127.0.0.1',port=8080) #定义web服务器运行的位置 端口
