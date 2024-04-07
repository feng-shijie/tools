import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
 
 #nvr    start 2023-09-01
 #oa1100 start 2023-02-01

nvr_path = "/home/rick/project/intellisight_nvr/nvr_codes/"
oa1100_path = "/home/rick/project/oa1100/"

list_nvr = list()       #nvr项目git提交次数列表
list_oa1100 = list()    #oa1100项目git提交次数列表
list_title = list()     #标题列表

save_img_oa1100 = '/home/rick/my/mypython3/oa1100.jpg'
save_img_nvr = '/home/rick/my/mypython3/nvr.jpg'

#指定开始时间和结束时间
date_s = None
date_e = None
date_s_cmd = "--since="
date_e_cmd = "--until="

#获取代码提交次数
git_s_cmd_count = "git log --author=fengshijie "
git_e_cmd_count = " --no-merges | grep -e \'commit [a-zA-Z0-9]*\' | wc -l"

#获取增加代码行数
git_e_cmd_row = " --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf loc }' -"

def save_img(_list, month_s, month_e, save_path):
    #添加图形属性
    plt.xlabel(list_title[0])
    plt.ylabel(list_title[1])
    plt.title(list_title[2])
    
    #bar函数中list数据要为int类型，才会自动排序
    first_bar = plt.bar(range(len(_list)), _list, color='g')  #初版柱形图，x轴0-9，y轴是列表y的数据，颜色是蓝色
    
    # 开始绘制x轴的数据
    list_index = list()
    list_name = list()
    for number in range(month_s, month_e):
        list_index.append(number - month_s)
        list_name.append(str(number) + " 月")
    plt.xticks(list_index, list_name) #绘制x轴的标签
    
    #柱形图顶端数值显示
    for data in first_bar:
        y = data.get_height()
        x = data.get_x()
        plt.text(x+0.15, y , str(y), va='bottom')  #0.15为偏移值，可以自己调整，正好在柱形图顶部正中

    #图片的显示及存储
    # plt.show()   #这个是图片显示
    # log = datetime.datetime.now().strftime('%Y-%m-%d')
    plt.savefig(save_path)   #图片的存储
    plt.close()   #关闭matplotlib


os.chdir(oa1100_path)
for number in range(2, 10):
    date_s = date_s_cmd + str(2023) + '-' + str(number) + '-' + str(1) + ' '
    date_e = date_e_cmd + str(2023) + '-' + str(number + 1) + '-' + str(1) + ' '
    cmd = git_s_cmd_count + date_s + date_e + git_e_cmd_count
    result = os.popen(cmd)
    val = result.readline()
    list_oa1100.append(int(val[0:len(val) - 1]))
    result.close()

date_s = date_s_cmd + '2023-02-1 '
date_e = date_e_cmd + '2023-12-31 '
cmd = git_s_cmd_count + date_s + date_e + git_e_cmd_row
result = os.popen(cmd)
count = result.readline()
result.close()

# print(list_oa1100)

list_title.append('每月的git提交次数\t总计增加代码: ' + count + ' 行')
list_title.append('')
list_title.append('oa1100 项目年度工作完成情况')

save_img(list_oa1100, 2, len(list_oa1100) + 2, save_img_oa1100)

os.chdir(nvr_path)
for number in range(9, 13):
    date_s = date_s_cmd + str(2023) + '-' + str(number) + '-' + str(1) + ' '
    date_e = date_e_cmd + str(2023) + '-' + str(number) + '-' + str(31) + ' '
    cmd = git_s_cmd_count + date_s + date_e + git_e_cmd_count
    result = os.popen(cmd)
    val = result.readline()
    list_nvr.append(int(val[0:len(val) - 1]))
    result.close()

date_s = date_s_cmd + '2023-09-1 '
date_e = date_e_cmd + '2023-12-31 '
cmd = git_s_cmd_count + date_s + date_e + git_e_cmd_row
result = os.popen(cmd)
count = result.readline()
result.close()

# print(list_nvr)

list_title.clear()
list_title.append('每月的git提交次数\t总计增加代码: ' + count + ' 行')
list_title.append('')
list_title.append('nvr 项目年度工作完成情况')

save_img(list_nvr, 9, len(list_nvr) + 9, save_img_nvr)