# zabbix_wechat

1、脚本运行顺序，获取zabbix传递过来的参数（wechat.sh）-->使用对应参数登录zabbix获取截图（image.py）-->发送微信消息（wechat.py）  
2、zabbix告警配置。  
   按顺序配置告警参数三个：  
    {ALERT.SENDTO}、{ALERT.SUBJECT}、{ALERT.MESSAGE}  
   告警内容：  
    1、Trigger status: {TRIGGER.STATUS}  
    2、Trigger severity: {TRIGGER.SEVERITY}  
    3、Event time:{EVENT.DATE}--{EVENT.TIME}  
    4、Item value:{ITEM.VALUE1}  
    5、Original item ID: {ITEM.ID}  
    6、Original event ID: {EVENT.ID}  
    告警脚本填写wechat.sh，收件人填写企业微信用户的用户名
3、事先将数据表zabbix.graphs_items中数据导出至/tmp/zabbix.txt  
    # /usr/bin/mysql -h127.0.0.1 -uzabbix -pzabbix@123 -e "select graphid,itemid from zabbix.graphs_items" > /tmp/zabbix.txt  
4、image中填入zabbix登录账号密码  
5、wechat.py中填入企业微信的corpid、secret、agentid即可  

图文告警图示  
![image](https://github.com/armolee/zabbix_wechat/blob/master/image_alert.png)  

卡片告警图示  
![image](https://github.com/armolee/zabbix_wechat/blob/master/card_alert.png)  


