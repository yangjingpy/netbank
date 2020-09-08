#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#auther:tester
#datetime:2020/8/5 13:45

import paramiko
import time

# class SSHConnection(object):
#     def __init__(self,hostname,port,name,password):
#         self.hostname = hostname
#         self.port = port
#         self.username = name
#         self.password = password
#     @property
#     def ssh_connect(self):
#         # 创建SSH对象
#         ssh = paramiko.SSHClient()
#         # 设置连接的远程主机没有本地主机密钥或HostKeys对象时的策略，目前支持三种：
#         # AutoAddPolicy
#         # 自动添加主机名及主机密钥到本地HostKeys对象，不依赖load_system_host_key的配置。即新建立ssh连接时不需要再输入yes或no进行确认
#         # WarningPolicy
#         # 用于记录一个未知的主机密钥的python警告。并接受，功能上和AutoAddPolicy类似，但是会提示是新连接
#         # RejectPolicy
#         # 自动拒绝未知的主机名和密钥，依赖load_system_host_key的配置。此为默认选项
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         # 连接服务器
#         ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
#         self.__ssh = ssh
#         print(self.__ssh)
#     def run_cmd(self,command):
#         """
#         执行shell命令,返回字典
#          return {'color': 'red','res':error}或
#          return {'color': 'green', 'res':res}
#         :param command:
#         :return:
#         """
#         stdin, stdout, stderr = self.__ssh.exec_command(command)
#         result = stdout.read().decode()  # 这个有问题，不显示错误，可以修改一下，先判断stdout有没有值，如果输出没有，就显示错误
#         err = stderr.read().decode()
#         if len(err) == 0:
#             return result
#         else:
#             return err
#
#
#     def close(self):
#         self.__ssh.close()
# if __name__=='__main__':
#     # 14:10.201.0.71
#     # 07:
#     ssh = SSHConnection('10.201.0.195',22,'root','linkwan')
#     # ssh = SSHConnection('10.201.0.71',22,'root','linkwan')
#     ssh.ssh_connect
#
#     # while True:
#     #     cmd = input("输入命令：")
#     #     if not cmd:
#     #         break
#     #     else:
#     #         print(ssh.run_cmd(cmd))
#     # ssh.run_cmd("sed -i '$a 121.199.198.169  iot.linkwan.cn' /etc/hosts")
#     print(ssh.run_cmd("swanctl --list-sas"))
#     ssh.close()


def verification_ssh(host,username,password,port,root_pwd,cmd):
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        ssh.send('sudo su\n')
        buff = ''
        while not buff.endswith('password for ubuntu: '):
            resp = ssh.recv(9999)
            buff +=str(resp,encoding='utf-8')
            # print(type(buff))
            # print(buff)
            # if buff.endswith('password for ubuntu: '):
            #     print('ture')
            # else:
            #     print('false')
            # print('+++++++')
        ssh.send(root_pwd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff += str(resp, encoding='utf-8')
            # print(type(buff))
            # print(buff)
            # if buff.endswith('# '):
            #     print('ture')
            # else:
            #     print('false')
            # print('+++++++')

        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff += str(resp, encoding='utf-8')
            print(type(buff))
            print(buff)
            # if buff.endswith('# '):
            #     print('ture')
            # else:
            #     print('false')
            # print('+++++++')
        s.close()
        result = buff
    else:
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
    return result
if __name__ == "__main__":
    a = verification_ssh('183.136.223.247', 'ubuntu', 'netbank.cn123', '22', 'netbank.cn123', 'swanctl --list-sas')
    print(type(a))

