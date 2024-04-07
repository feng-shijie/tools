#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys

m_file = "tmp.xml"

if len(sys.argv) < 3:
    print('''
        功能：：
            # xml多个标签一样值却不一样
            xml按标签取出其中的值
            此程序会打开指定xml文件逐行获取指定标签的值写入tmp.xml文件中<默认结果是去重的>
        去重：：
            1.字符串重复
            2.字母相同带:的
        使用方法：：
            python3 getXmlAllVal.py file.xml xml_key
        参数解释：:
            file.xml    xml文件
            xml_key     xml key值 在程序中会拼接成</xml_key>
        问题：
            如果标签不再同两行内可能会出错
        ''')
    exit()

m_xml            = sys.argv[1]
m_xml_end_key    = "</" + sys.argv[2] + ">"
m_key_end_size   = len(m_xml_end_key)
m_xml_begin_key  = "<"  + sys.argv[2] + ">"
m_key_begin_size = len(m_xml_begin_key)

m_format = "{0:<25}\t{1:<10}\t{2:<5}"

if os.path.exists(m_file):  os.system("rm -f " + m_file)
m_fp_xml = open(m_xml, "r")
m_str    = m_fp_xml.readline()

if not m_str:
    print(m_file,"文件是空的,请按要求添加路径后重试\n\n")
    exit()

only_list = {}
count     = 0
print(m_format.format("key 值为 ", ':', m_xml_end_key))

#把xml文件中的所有值写入tmp.xml中
while m_str:
    m_str = m_str.strip()
    m_str = m_str.strip('\n')

    if m_str.rfind(m_xml_end_key, len(m_str) - m_key_end_size, len(m_str)) > 0:
        s_index = m_str.find('>', 0, len(m_str) - m_key_end_size)
        #去重
        str_name = m_str[(s_index+1): len(m_str) - m_key_end_size]
        str_name = str_name.strip()     #过滤名字相同带空格的
        if str_name:
            name_lower = str_name.lower()
            #过滤名字相同带冒号的   中文标点符号与英文的不同
            if name_lower[len(name_lower) - 1] == ':' or name_lower[len(name_lower) - 1] == '：':
                if only_list.get(name_lower[0 : len(name_lower) - 1]) == None:
                    only_list[name_lower[0 : len(name_lower) - 1]] = str_name   #key值修改为去掉冒号的值
            elif only_list.get(name_lower) == None:   only_list[name_lower] = str_name
            else:  #key相同优先使用大写的或值较小的
                if only_list[name_lower] > str_name:
                    only_list[name_lower] = str_name
            count += 1
    elif m_str.find(m_xml_begin_key, 0, m_key_begin_size) >= 0:
        m_str += ' ' + m_fp_xml.readline().strip()
        continue
    m_str = m_fp_xml.readline()

m_fp_xml.close()
print(m_format.format("xml val count ", ':', count))

count = 0
m_fp = open(m_file, 'w')
for key in only_list:
    # val = str(count).zfill(4)
    # m_fp.write('\t' + ("<OL" + val + '>') + str(key) + ("</OL" + val + '>') + '\n')
    count += 1
    m_fp.write(str(only_list[key]) + '\n')

m_fp.close()
print(m_format.format("xml val 去重后的总数 ", ':', count))
print(" 完成! ")
