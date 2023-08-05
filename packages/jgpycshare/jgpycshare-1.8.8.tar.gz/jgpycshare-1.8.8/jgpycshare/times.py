import http.client
import time
import os
# import tools.holiday

def get_webservertime(host='www.baidu.com'):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    # print(ltime)
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    now = time.strftime("%Y-%m-%d %H:%M:%S", ttime)
    # print(now)
    return now


# def StockRunTime():
#     isdo = False
#     nowt = time.strftime("%H%M%S", time.localtime())
#     nowt = int(nowt)
#     # 工作日
#     if tools.holiday.IsWorkDay():
#         if nowt >= 93000 and nowt <= 113000:
#             isdo = True
#         if nowt >= 130000 and nowt < 150000:
#             isdo = True
#     else:
#         print('不是工作日')

#     return isdo