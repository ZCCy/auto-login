import requests
import pywifi
from pywifi import const
import time
from urllib import request
import socket

connect_wifi_name = "NJUPT-CMCC"/"CHAINANET"
const.IFACE_DISCONNECTED = 0 #没有连接
const.IFACE_SCANNING = 1 #扫描中
const.IFACE_INACTIVE = 2 #没有激活
const.IFACE_CONNECTING = 3 #连接中
const.IFACE_CONNECTED = 4 #已连接


#多网卡情况下，根据前缀获取IP
def GetLocalIPByPrefix(prefix):
	localIP = ''
	for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
		if ip.startswith(prefix):
			localIP = ip
	
	return localIP	
print(GetLocalIPByPrefix('10.163'))
ip=GetLocalIPByPrefix('10.163')

def login():
    url='http://p.njupt.edu.cn:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=p.njupt.edu.cn&iTermType=1&wlanuserip='+ip+'&wlanacip=10.255.252.150&wlanacname=XL-BRAS-SR8806-X&mac=00-00-00-00-00-00&ip='+ip+'&enAdvert=0&queryACIP=0&loginMethod=1'
    print(url)
    postdata={
         "DDDDD" : ",0,学号@cmcc/jwty（移动/电信）",
         "upass" : "密码",
         "R1" : "0",
         "R2" : "0",
         "R3" : "0",
         "R6" : "0",
         "para" : "00",
         "0MKKey" : "123456",
         "buttonClicked" : "",
         "redirect_url" : "",
         "err_flag" : "",
         "username" : "",
         "password" : "",
         "user" : "",
         "cmd" : "",
         "Login" : "",
         "v6ip" : "",
    }
    requests.post(url,data=postdata)

    
testUrl = "https://www.baidu.com" #以百度为测试目标
def testNetwork():
    try:
        ret = request.urlopen(url=testUrl, timeout=3.0)
        print("网络已连接")
    except:
        print("网络未连接，请进行下一步操作")
        return False
    return True

def connectWifi():
    print("进入")
    wifi = pywifi.PyWiFi()  # 创建一个无线对象
    ifaces = wifi.interfaces()  # 获取pc机的无线网卡
    
    iface = ifaces[0]  # 取第一个无线网卡
    
    profiles = iface.network_profiles() #获取pc机此前连接过的所有wifi的配置profile
    for item in profiles:
        if item.ssid == connect_wifi_name: # 连接目标wifi
           # temp_profile=iface.add_network_profile(item)  # 设定连接文件
            iface.connect(item)  # 开始连接wifi
            time.sleep(5) #等待3秒钟
            break #跳出循环
    
    login()
    if iface.status() == const.IFACE_CONNECTED: #判断连接状态是否为4
        print("连接已有配置成功")
        if testNetwork(): #测试是否能上外网
            print("开始上网吧~")
        else:
            print("开始准备打开浏览器")
            
    else:
        # getWifi(iface) #该方法以后会有妙用，不过这里先注释掉
        print("连接已有配置失败，开始尝试连接新的wifi")

print("开始")
if __name__ == "__main__":
    connectWifi()