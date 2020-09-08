#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
import json
# from robot.api import logger
from requests_toolbelt import MultipartEncoder
import os
import re

import xlwt

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Sheet1')

METHODS = ['GET','POST','PUT','DELETE']
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
DOWN_FILE_BASE = r'C:\Users\tester\Desktop'

class UnSupportMethodException(Exception):
    """当传入的method的参数不是支持的类型时抛出此异常。"""
    pass


class ApiRequest(object):
    headers = {"Content-Type": "application/json"}
    def __init__(self,headers=None,cookies=None):
        self.session = requests.session()
        self._set_headers(headers)
        self._set_cookies(cookies)

    def _set_headers(self,headers):
        if headers:
            self.session.headers.clear()
            self.session.headers.update(headers)

    def _set_cookies(self,cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, url=None, method='POST', params=None, data=None, **kwargs):
        # print('---------------------')
        # print(url)
        # print(type(url))
        # if '?' in url:
        #     print('++++++++++++++++++++++++++++++')
        #     b = re.split('\?',url)
        #     params = b[1]

        if method.upper() not in METHODS:
            raise UnSupportMethodException('不支持的method:{0}，请检查传入参数！'.format(method))
        if type(data) != str:
            data = json.dumps(data)
        logging.info('请求 : ' + method)
        logging.info('地址 : ' + url)
        logging.info('HEAD : ' + str(self.session.headers))
        logging.info('参数 : ' + data)
        response = self.session.request(url=url, method=method,params=params, data=data,headers=self._set_headers(self.headers),verify=False, **kwargs)
        response.encoding = 'utf-8'
        logging.info('{0} {1}'.format(method, url))
        logging.info('请求结果: {0} '.format(response.text))
        self._isOk(response)
        response.close()
        return (response.status_code,self._response(response))

    def upload_file(self,url,file_path,bizType=None):

        file_type = {
            'zip': 'application/zip',
            'png': 'image/png',
            'jpeg': 'image/jpeg',
            'xlsx': 'text/xlsx'
        }
        filename = os.path.basename(file_path)
        f1 = filename.rsplit('.',1)[1]
        logging.info(f1)
        try:
            f2 = file_type[f1]
            print(f2)
        except KeyError:
            raise 'file type is not file_type'
        except Exception as e:
            logging.error(e)
        else:
            print(repr(filename))
            m = MultipartEncoder(
                fields={
                    'bizType': bizType,
                    'file': (filename, open(file_path, 'rb'), f2)
                }
            )

            headers = {"Content-Type": m.content_type}
            response = self.session.post(url, data=m,
                                  headers=self._set_headers(headers), verify=False)
            response.encoding = 'utf-8'
            logging.info(url)
            logging.info('请求结果: {0} '.format(response.text))
            self._isOk(response)
            response.close()
            return (response.status_code,self._response(response))

    def download_file(self,url,file_name):
        """
        download files and save it in DOWN_FILE_BASE
        :param url:
        :param file_name:like sn.xlsx,images.bin
        :return:
        """
        headers = {'Accept-Encoding': 'gzip, deflate, br'}
        file_path = DOWN_FILE_BASE + '\\'+file_name

        response = self.session.get(url, params=None, data=None,
                                     headers=self._set_headers(headers), verify=False)
        response.encoding = 'utf-8'
        logging.info(url)
        logging.info('请求结果: {0} '.format(response.text))
        self._isOk(response)
        response.close()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return (response.status_code, self._response(response))

    def _isOk(self, response):
        '''
        check the response
        :param response:
        :return:
        '''

        try:
           json_formated = json.dumps(json.loads(response.text),ensure_ascii=False,indent=2)
        except:
           json_formated = response.text
        if response.status_code not in [200,201,202,203,204,205,206,207]:
            logging.error(json_formated)
        else:
            logging.debug(json_formated)

    def _response(self,response):
        try:
            #把json字符串解码为python对象
            res = json.loads(response.text)
            print('----------------')
        except Exception as e:
            res = response.text
            print('++++++++++++++++++++++==')
        return res

if __name__=='__main__':
    para = {
        "username": "wanghongliang@netbank.cn",
        "password": "4285s92ak2"}

    api = ApiRequest()

    code,res = api.send(method='post',url='https://test.linkwan.cn/proxy/auth/login',data=para)
    ##升级
    para ={
        "snList": ["V501202009010001"],
        "version": "v4.0.0-14-g49336e8-20200831_DEBUG"
    }
    code, res = api.send(method='post', url='https://test.linkwan.cn/proxy/major/api/equipment/batchUp', data=para)
    print(res['mainTaskId'])
    task_id = res['mainTaskId']
    ##获得任务ip,判断升级是否成功
    code, res = api.send(method='get', url='https://test.linkwan.cn/proxy/configuration/api/device-config-histories?size=10&page=0&sort=id,desc&queryCondition=%s'%task_id)
    while res['content'][0]['status'] == 'START':
        code, res = api.send(method='get',
                             url='https://test.linkwan.cn/proxy/configuration/api/device-config-histories?size=10&page=0&sort=id,desc&queryCondition=%s'%task_id)



