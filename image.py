#!/usr/local/bin/python
# coding = utf-8
# name image.py
# 获取对应item的graph，若对应item无graph则获取近期数值的截图
import time
from selenium import webdriver
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 登录zabbix获取截图
def get_item_graph(itemid,flag,image):
	
	driver = webdriver.PhantomJS("/usr/local/phantomjs-2.1.1/bin/phantomjs")
        driver.get("http://127.0.0.1/zabbix/")
	driver.set_window_size(640, 480)
	driver.find_element_by_id("name").send_keys("admin")
	driver.find_element_by_id("password").send_keys("zabbix")
	driver.find_element_by_id("enter").click()
	if flag:
		driver.get("http://127.0.0.1/zabbix/history.php?action=showgraph&fullscreen=1&itemids[]="+itemid)
        else:
		driver.get("http://127.0.0.1/zabbix/history.php?action=showvalues&fullscreen=1&itemids[]="+itemid)
        time.sleep(2)
        driver.save_screenshot(image)
	driver.close()
	driver.quit()
	
if __name__ == "__main__":
    if len(sys.argv) > 1:
        itemid = sys.argv[1]
        flag = sys.argv[2]
        image = sys.argv[3]
	get_item_graph(itemid,flag,image)
