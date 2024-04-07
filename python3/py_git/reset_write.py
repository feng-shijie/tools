#!/usr/bin/env/python
#-*- coding:utf-8 -*-

#根据绝对路径 使用temp文件覆盖原始文件
import os

m_file = "/home/rick/tempgit.txt"
m_dir = "/home/rick/tempgit/"
if not os.path.exists(m_dir):
    print("tempgit 目录不存在，请执行 reset_read.py 文件 ！")
    exit()

m_fp = open(m_file, 'r')
m_str = m_fp.readline()

#cp temp目录到原文件
while m_str:
    m_str = m_str.strip('\n')
    m_str = m_str.strip()
    m_list = m_str.split('/')
    m_len = len(m_list)
    temp_dir = None
    temp_dir = m_dir + m_list[m_len-2] + '/'

    m_cmd = None
    m_cmd = "cp " + temp_dir + m_list[m_len-1] + ' ' + m_str
    print(m_cmd)
    #os.system(m_cmd)
    m_str = m_fp.readline()
m_cmd = "rm -rf " + m_dir
os.system(m_cmd)

m_cmd = "rm -f " + m_file
os.system(m_cmd)

print(m_dir, "删除成功" )
print(m_file, "删除成功")
print("write 成功！")
