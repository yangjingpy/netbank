# -*- coding:utf-8 -*-
#__author__ = 'yangjing'
import re

PATH = r'C:\Users\tester\Desktop\sd.txt'

def read_file(path):
    """
    read sd.txt,return list
    :param path:
    :return:
    """
    stu_list = []
    with open(PATH, 'r', ) as f:
        for i in f.readlines():
            stu_list.append(i)
    return stu_list


def _modify_data(stu_list:list):
    """
    [xx,xx] to [{'name':'xxx','score':'90'}],remove spaces and line breaks
    :param stu_list:
    :return:
    """
    stu_list_new = []
    for i in stu_list:
        stu_dict = dict()
        ###get name,and score values
        name = re.search('name:(.*);', i)
        score = re.search('score.*:(.*\d*)', i)
        if name and score:
            stu_dict['name'] = (name.group(1)).strip()
            stu_dict['score'] = (score.group(1)).strip()
            stu_list_new.append(stu_dict)
    return stu_list_new

def _score_sort(stu_list_new):
    """
    according to score ,and sort,[{'name':'xxx','score':'90'},{'name':'xxx','score':'60'}]
    :param stu_list_new:
    :return:
    """
    score_list = []
    for i in stu_list_new:
        score_list.append(int(i['score']))
    ###score_list ,sorted order
    score_list_new = sorted(score_list, reverse=True)
    ####according to score_list ,sort
    last_stu = []
    for i in score_list_new:
        for j in stu_list_new:
            print(j)
            if i == int(j['score']):
                last_stu.append(j)
    return last_stu

def _standard_format(last_stu):
    """
    name :align left ,score:center,score values :right
    :param last_stu:
    :return:
    """
    last_stu_list = []
    for i in last_stu:
        new_name = 'name:' + i['name']
        new_scroe = ';score:'
        ###str --align left:ljust;right---rjust
        new_str = new_name.ljust(20) + new_scroe + i['score'].rjust(10)
        last_stu_list.append(new_str)
    return last_stu_list

def gen_file(path,last_stu_list):
    """
    generate file
    :param path:
    :param last_stu_list:
    :return:
    """
    with open(path,'w') as f:
        for i in last_stu_list:
            f.write(i)
            f.write('\n')

stu_list = read_file(PATH)
stu_list_new = _modify_data(stu_list)
last_stu =_score_sort(stu_list_new)
last_stu_list =_standard_format(last_stu)
gen_file(r'C:\Users\tester\Desktop\sd-new.txt',last_stu_list)
