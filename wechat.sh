#!/bin/bash
# name:wechat.sh

# zabbix传过来的三个参数 {ALERT.SENDTO}、{ALERT.SUBJECT}、{ALERT.MESSAGE}
send_to=$1
subject=$2
message=$3

# zabbix报警信息内容
#<p>1、Trigger status: {TRIGGER.STATUS}</p>
#<p>2、Trigger severity: {TRIGGER.SEVERITY}</p>
#<p>3、Event time:{EVENT.DATE}--{EVENT.TIME}</p>
#<p>4、Item value:{ITEM.VALUE1}</p>
#<p>5、Original item ID: {ITEM.ID}</p>
#<p>6、Original event ID: {EVENT.ID}</p>

# 从zabbix报警信息中获取对应的itemid,eventid。stat存储此次事件为PROBLEM还是OK状态
itemid=`echo $message | egrep -o "item ID: [0-9]*"| awk '{print $NF}'`
eventid=`echo $message | egrep -o "event ID: [0-9]*"| awk '{print $NF}'`
stat=`echo $message | egrep -o "Trigger status: PROBLEM|Trigger status: OK"| awk '{print $NF}'`

# 定义图片保存位置
image=/tmp/$eventid"_"$stat".png"


# 从数据库中获取itemid是否有对应的graphid。以flag标识有无。事先将数据表zabbix.graphs_items中数据导出至/tmp/zabbix.txt
# /usr/bin/mysql -h127.0.0.1 -uzabbix -pzabbix@123 -e "select graphid,itemid from zabbix.graphs_items" > /tmp/zabbix.txt
graphid=`/bin/cat /tmp/zabbix.txt | awk '{ if($2=="'"$itemid"'"){print $1}}'`
if [ ! $graphid ]
then
	flag=0
else
	flag=1
fi

cd /usr/local/zabbix/share/zabbix/alertscripts/
# image.py 使用获取到的graphid获取截图信息，将图片信息保存至image
./image.py "$itemid" "$flag" "$image"

# 发送image 信息到微信接口
./wechat.py "$send_to" "$subject" "$message" "$image" "$itemid"
# 记录日志并删除图像信息
echo $image >> /tmp/zabbix_event.log && /bin/rm -f $image
