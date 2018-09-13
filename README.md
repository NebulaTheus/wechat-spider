# wechat-spider
微信公众号爬虫-2018.9

目标：抓取微信公众号的全部历史文章的标题和url，保存到本地csv。

实现：利用anyproxy抓包手机微信app，获取其发送请求时的appmsg_token和cookie,发送给爬虫代码，用以构造请求。主要用到的工具有anyproxy抓包工具，adb安卓调试工具用以实现电脑对手机的操控（微信公众号历史页面的点击进入）。aiohttp搭建一个简单的本地web服务用以实现anyproxy和爬虫程序的通信。
weixin_spider.py为爬虫主程序，sample.js为基于nodejs编写的anyproxy中间件（二次开发，获取APP的请求参数），aiohttp_web.py为本地web服务。

详细内容参见博客：https://blog.csdn.net/xing851483876/article/details/82493412

## 欢迎关注个人公众号，更多爬虫案例持续更新！

![二维码](https://github.com/NebulaTheus/wechat-spider/blob/master/code.jpg)
