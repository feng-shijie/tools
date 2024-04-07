#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys

if len(sys.argv) < 1:
    print('''
        功能：：
        字符串格式化<首字母优化为大写>：
            1.空格字符后面首字母优化为大写
            2.特殊字符后面首字母也是优化为大写
            3.如果大写字母前面没有空格则增加<第一个首字母除外>
        使用方法：：
            python3 strFormat.py file bool
        参数解释：:
            file    要解析的文件
            bool    True: txt格式    <默认为 xml格式>

        输出：： strFormat.xml/strFormat.txt 文件
        ''')
    exit()

m_new_file = "strFormat.xml"
if len(sys.argv) > 2:
    if sys.argv[2] == "True":   m_new_file = "strFormat.xml"
    else:                       m_new_file = "strFormat.txt"

m_fp  = open(sys.argv[1], "r")
m_str = m_fp.readline()

if not m_str:
    print(m_new_file,"文件是空的,请按要求添加路径后重试\n\n")
    m_fp.close()
    exit()

if os.path.exists(m_new_file):  os.system("rm -f " + m_new_file)

m_new_fp = open(m_new_file, 'w')

#把xml文件中的所有值写入space.xml中
while m_str:
    m_new_str = str()
    b_space   = False           #上一个字符是否为空格
    b_big     = True            #上一个字符是否为大写
    b_other   = False           #上一个字符不是字母
    m_str     = m_str.strip()
    m_str     = m_str.strip('\n')

    if len(m_str.split(' ')) > 2:
        m_new_fp.write(m_str + '\n')
        m_str = m_fp.readline()
        continue

    for index in range(0, len(m_str)):
        if m_str[index] == ' ':
            b_space    = True
            m_new_str += ' '
            continue

        b_up = False
        #当前字母是否为小写
        if m_str[index] >= 'a' and m_str[index] <= 'z':
            if b_space or b_other or index == 0:    b_up = True
            if index != 0: b_big = False
            b_other = False
        elif m_str[index] < 'A' or m_str[index] > 'Z':  b_other = True
        else:
            if b_space == False and b_big == False and b_other == False:     m_new_str += ' '
            b_big   = True
            b_other = False

        if b_up:    m_new_str += m_str[index].upper()
        else:       m_new_str += m_str[index]
        b_space = False


    m_str = m_fp.readline()
    m_new_fp.write(m_new_str + '\n')

m_fp.close()
m_new_fp.close()
print(" 完成! ")