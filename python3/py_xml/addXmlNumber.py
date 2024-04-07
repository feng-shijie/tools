#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys

if len(sys.argv) < 3:
    print('''
        功能：：
            把文件中的字符串改成合理的xml格式
        使用方法：：
            python3 addXmlNumber.py file.xml xml_label_name custom_name
        参数解释：:
            file.xml        xml文件
            xml_label_name  如输入::olb  将会输出::<olb001>temp</olb001>
            custom_name     默认为<xml_label_name001>,为True则是<xml_label_name>
        ''')
    exit()

m_new_file = "number.xml"
if os.path.exists(m_new_file):  os.system("rm -f " + m_new_file)
m_fp = open(sys.argv[1], "r")
m_str    = m_fp.readline()

if not m_str:
    print(m_fp,"文件是空的,请按要求添加路径后重试\n\n")
    exit()

b_type = False
if len(sys.argv) >= 4:
    if sys.argv[3] == "True":   b_type = True
s_label = sys.argv[2]
count = 0
m_new_fp = open(m_new_file, 'w')

while m_str:
    m_str = m_str.strip('\n')
    if b_type:
        s_head = "<"  + s_label + '>'
        s_end  = "</" + s_label + '>'
        s_new_str = s_head + str(m_str) + s_end + '\n'
    else:
        val = str(count).zfill(4)
        s_head = "<"  + s_label + val + '>'
        s_end  = "</" + s_label + val + '>'
        s_new_str = "\t\t" + s_head + str(m_str) + s_end + '\n'
        count += 1
    m_new_fp.write(s_new_str)
    m_str  = m_fp.readline()

m_fp.close()
m_new_fp.close()
print(" 完成! ")
