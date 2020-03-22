#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import socket
import time
import json
import time
ddns_params = dict(
    #   动态域名解析借口传参，具体看官网的接口文档
    login_token="userid,token",  # 这里请从管网去设置
    format="json",
    domain_id=82800057,  # 调用getDomainList 获取 并写入
    record_id=559488514,  # 调用list 获取
    sub_domain="@",  # 改为直接指向域名
    record_line_id=0,
)

record_params = dict(
    #   请求域名ID为56731616的域名的记录传参，具体看官网的接口文档
    login_token="userid,token",  # replace with your login_token
    format="json",
    domain_id=82800057,  # replace with your domain_od, can get it by API Domain.List
)

current_ip = None


def ddns(ip):
    #     调用动态域名解析接口
    ddns_params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    rs=requests.post(' https://dnsapi.cn/Record.Ddns',data=ddns_params,headers=headers)
    print(rs.text)



def getip():
    #   获取本地外网ID
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip


def getRecordip():
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    rs = requests.post('https://dnsapi.cn/Record.List',data=record_params,headers=headers)
    data = json.loads(rs.text)
    record_list = data.get('records')
    for r in record_list:
        if r.get('id') == ddns_params['record_id']:
            return r.get('value')
    return None

def getDomainList():
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    rs = requests.post('https://dnsapi.cn/Domain.List', data=record_params, headers=headers)
    data = json.loads(rs.text)
    print(data)
if __name__ == '__main__':
    #获取域名列表
    # getDomainList()
    while True:
        try:
            current_time = time.strftime('%Y%m%d%H%M',
                                         time.localtime(time.time()))  # 返回当前时间
            current_ip = getRecordip()
            print(current_time)
            print("当前设置ip："+current_ip)
            ip = getip()
            ip=bytes.decode(ip)
            print("当前外网ip="+ip)
            if current_ip != ip:
                if ddns(ip):
                    current_ip = ip
        except Exception as e:
            print(e)
            # raise e
            pass
        time.sleep(300)
