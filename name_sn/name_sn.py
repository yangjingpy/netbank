#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#auther:tester
#datetime:2020/8/12 15:43
from ApiRequest import ApiRequest
from ssh_hosts import verification_ssh
import re
#ssh登录vpe，获取所有的vti的id
res = verification_ssh('183.136.223.246', 'ubuntu', 'netbank.cn123', '22', 'netbank.cn123', 'swanctl --list-sas')
print(res)
#re.MULTILINE匹配多行，若不加，当有多行返回值时，就无法匹配
comment = re.compile(r'(^b.+): #',re.MULTILINE)
vti_id = re.findall(comment,res)
print(len(vti_id))
print(vti_id)

#使用http请求的方式获取etcd中vti id对应的设备号
api = ApiRequest()
name_sn = dict()
for i in vti_id:
    code, res = api.send(method='get',
                         url='http://47.98.131.158:30333/v3/get?key=/registry/ipsec/v1/default/%s'%i)

    #匹配channelId: V501202007141416后的16位，可以换行匹配
    comment = re.compile(r'channelId: (.{16})', re.MULTILINE)
    try:
        sn = re.findall(comment,res['node']['value'])
    except KeyError:
        print('etcd 不存在')
    sn_str = "".join(sn)
    name_sn[i]=sn_str
    # print(res['node']['value'])

print(name_sn)
print(len(vti_id))
print(vti_id)

###使用接口查看nms的vpe包括的cpe
para = {
        "username": "admin",
        "password": "sdwan123!@#"}

code,res = api.send(method='post',url='http://test.linkwan.cn//proxy/auth/login',data=para)

code,res = api.send(method='get',url='http://test.linkwan.cn/proxy/major/api/vpes/getLinkList?size=50&page=0&vpeId=8&isRefresh=true')
api_sn = []
for i in range(len(res['content'])):
    api_sn.append(res['content'][i]['sn'])

print('vpe的隧道个数'+ str(len(vti_id)))
print(vti_id)
print(name_sn)
print(api_sn)
print('api接口返回页面的统计数据'+str(len(api_sn)))
print('etcd中有'+ str(len(name_sn.values())))
#合集
last_sn=[value for value in name_sn.values() if value in api_sn]
print('不存在：')
print(set(api_sn)-set(name_sn.values()))
print('存在的')
print(last_sn)