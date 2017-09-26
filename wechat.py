#!/usr/local/bin/python
#_*_coding:utf-8 _*_
import requests,sys,json
import urllib3
urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')


def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url,params=Data,verify=False)
    Token = r.json()['access_token']
    return Token

def GetImageUrl(Token,Path):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % Token
    data = {
        "media": open(Path,'r')
        }
    r = requests.post(url=Url,files=data)
    dict = r.json()
    return dict['media_id']

#发送文字消息
def SendMessage(Token,User,Agentid,Subject,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                                             
        "msgtype": "text",                            
        "agentid": Agentid,                           
        "text": {
            "content": Subject + '\n' + Content
        },
        "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

# 发送卡片信息
def SendCardMessage(Token,User,Agentid,Subject,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                               
        #"totag": Tagid,                               
        "msgtype": "textcard",                         
        "agentid": Agentid,                           
        "textcard": {
            "title": Subject,
            "description": Content,
            "url": "http://127.0.0.1/zabbix/",
            "btntxt": "详情"
        },
        "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text


# 发送图文信息
def SendnewsMessage(Token,User,Agentid,Subject,Content,Image,Itemid):
    Url = "http://127.0.0.1/zabbix/history.php?action=showgraph&fullscreen=1&itemids[]="+Itemid
    Data = {
        "touser": User,                             
        "msgtype": "mpnews",                           
        "agentid": Agentid,                             
        "mpnews": {
            "articles": [
                {
                    "title": Subject,
                    "thumb_media_id": Image,
                    "content": Content,
                    "content_source_url": Url,
                    "digest": Content
                }
            ]
        },
        "safe": "0"
    }
    headers = {'content-type': 'application/json'}
    data = json.dumps(Data,ensure_ascii=False).encode('utf-8')
    r = requests.post(url=Url,headers=headers,data=data)
    return r.text


if __name__ == '__main__':
    User = sys.argv[1]                                                             
    Subject = sys.argv[2]                                                          
    Content = sys.argv[3]                                                           
    Path = sys.argv[4]							            						
    Itemid = sys.argv[5]
    Corpid = "xxxxxx"                          # CorpID是企业号的标识
    Secret = "xxxxxx"                          # Secret是管理组凭证密钥
    Agentid = "xxxxxx"                         # 应用ID

	#获取token
    Token = GetToken(Corpid, Secret)
	#上传临时素材
    Image = GetImageUrl(Token,Path) 
	#发送消息
    Status = SendnewsMessage(Token,User,Agentid,Subject,Content,Image,Itemid)
