#!/usr/bin/python
# coding: utf-8
# Date 2021/7/20
from flask import Flask,request,session
app = Flask(__name__)
app.config["SECRET_KEY"] = "131"

import requests
appID='xxx'
appsecret='xxx'
template_id="xxxx"

def get_acctoken():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appID + "&secret=" + appsecret
    r = requests.get(url)
    if 'access_token' in r.json():
        return r.json()['access_token']
    else:
        return False

def send_tomsg(token,title,body,touserid):
    data={"touser":touserid,
        "url":"https://www.baidu.com",
        "template_id":template_id,
        "topcolor":"#FF0000",
        "data":{"title1":
                        {"value":"标题:\t\t\t\t"+title,"color":"#A8A8A8"},
                "title2":
                        {"value":"通知内容:\t\t\t\t","color":"#A8A8A8"},
                "title3":
                        {"value":"通知时间:\t\t\t\t","color":"#A8A8A8"},
                "title4":
                        {"value":"备注:\t\t\t\t","color":"#A8A8A8"},
                "content1":
                        {"value":str(body)+"\n"},
                "content2":
                        {"value":"2021-11-17 16:19:36\n"},
                "content3": {"value":"本次推送由print支持\n"}}}
    url_vx = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + token
    data2=requests.post(url_vx, json=data).json()
    if data2['errmsg']=='ok':
        return True
    else:
        return False

@app.route("/msg/")
def test():
    title = request.args.get("title")
    body = request.args.get("body")
    touserid=request.args.get("touserid")
    if not session.get("acctoken"):
        session['acctoken']=get_acctoken()
    print(session.get("acctoken"))
    if session.get("acctoken"):
        if send_tomsg(session.get("acctoken"),title,body,touserid):
            return "发送成功"
        else:
            return "发送失败"
    else:
        return 'acctoken error'
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9916,debug=True)

