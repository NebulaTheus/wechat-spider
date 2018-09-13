
var http = require('http'); //引用http模块
var querystring = require('querystring');//引用querystring模块
//构造一个函数，用于发送post请求，发送的内容为contents
function post_data(contents) {
    var options = {
        host: '127.0.0.1',
        port: '8080',
        path: '/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': contents.length }
    }

    var req = http.request(options, function (res) {
        res.setEncoding('utf8');
        res.on('data', function (data) {
            console.log("data:", data);
        });
    });
    req.write(contents);
    req.end;
}


//anyproxy固定格式
module.exports = {
  summary: 'a rule to get url and cookie', //一段代码功能介绍
    //在request发送前执行，下面的if通过正则匹配请求的url来找到加载更多的请求，然后获取url、cookie
  *beforeSendRequest(requestDetail) {
    if (/mp.weixin.qq.com\/mp\/profile_ext\?action=getmsg&__biz/i.test(requestDetail.url)) {
        console.log('***********抓取到目标**********')
        console.log(requestDetail.requestOptions['headers'])
        var contents=querystring.stringify({
             'url':requestDetail.url,
             'cookie':requestDetail.requestOptions['headers']['Cookie']});
        post_data(contents) //发送post请求


        return null

    }

  },
};











