#!/usr/bin/env/python
#-*- coding:utf-8 -*-

#把要保存的文件cp到temp dir中做temp save
import os

m_file = "/home/rick/tempgit.txt"
m_dir = "/home/rick/tempgit/"
m_cmd = None

print('''
    功能：：
    复制当前分支文件到最新分支！
    启动本脚本将自动复制所需文件到/home/rick/tempgit/目录下,执行reset_write程序将覆盖原来的文件
    需手动通过vs获取你要复制文件的绝对路径加载至/home/rick/tempgit.txt 文件中
    ''')
if not os.path.exists(m_file):
    m_cmd = "touch " + m_file
    os.system(m_cmd)
    m_cmd = "mkdir -p " + m_dir
    os.system(m_cmd)
    print("/home/rick/tempgit.txt 文件以创建！")
    exit()

m_fp = open(m_file, 'r')
m_str = m_fp.readline()

if not m_str:
    print(m_file,"文件是空的,请按要求添加路径后重试\n\n")
    exit()

#cp 源文件到temp目录
while m_str:
    m_str = m_str.strip('\n')
    m_str = m_str.strip()
    m_list = m_str.split('/')
    m_len = len(m_list)
    temp_dir = None
    temp_dir = m_dir + m_list[m_len-2] + '/'

    m_cmd = "mkdir -p " + temp_dir
    os.system(m_cmd)
    # print(m_cmd)


    m_cmd = "cp " + m_str + ' ' + temp_dir + m_list[m_len-1]
    # print(m_cmd)
    os.system(m_cmd)
    # print(m_str,temp_dir+m_list[m_len-1])
    m_str = m_fp.readline()

print("cp 成功！")

