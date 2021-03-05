# -*- codeing= utf-8 -*-
# @Time :2021/2/8 12:28
# @Author:黄国彬
# @File:PaChinese.py
# @Software:PyCharm
# 读取Java文件中的中文，忽略注释
import re
import os

import xlwt

# 匹配中文
prompt = re.compile(r'prompt="[\u4e00-\u9fa5]*"')
text = re.compile(r'text="[\u4e00-\u9fa5]*"')
require = re.compile(r'requiredMessage="[\u4e00-\u9fa5]*"')
datapattern = []
datapattern.append(prompt)
datapattern.append(text)
datapattern.append(require)


# def DiGuiGetPath(path):
#     filesList = os.listdir(path) # 返回一个由文件名和目录名组成的列表
#     print(filesList)
#     for fileName in filesList:
#         fileAbpath = os.path.join(path, fileName)
#         if os.path.isdir(fileAbpath):#如果是目录
#             print("目录：", fileName)
#             DiGuiGetPath(fileAbpath)
#         else:
#             print("普通文件", fileName)
#
#     # 传递参数的时候，注意需要写上（r）表明传递的是路径

def main():
    path = ".\\a.java"
    # path = DiGuiGetPath(r"E:\code\shixun\work\venv")
    datalist = findChinese(path)
    # datalist=str(datalist)#存入excel 写出字符串
    print(type(datalist))
    savepath = ".\\爬取中文.xls"
    saveDate(datalist, savepath)


def findChinese(path):
    # 返回结果
    datalist = []
    file = open(path, encoding="UTF-8")
    strfile = file.read()

    # 遍历字符串，一次处理一行
    for line in strfile.slitlines():

        for i in range(len(datapattern)):
            re = datapattern[i].findall(line)
            if len(re) != 0:

                datalist.append(re)

        # rel111 = pa1.findall(line)
        # if len(rel111) != 0:
        #     # print(rel111)#输出每一行的中文
        #     datalist.append(rel111)
        #
        #
        #
    #
    #     rel112 = pa2.findall(line)
    #     print(rel112)
    #
    #     if len(rel112) != 0:
    #         # print(rel111)#输出每一行的中文
    #         datalist.append(rel112)
    # for i in range(len(datalist)):
    #     print(datalist[i])

    file.close()
    print(datalist)
    return datalist


def saveDate(datalist, savepath):
    # k=1
    # book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # sheet = book.add_sheet('paqu', cell_overwrite_ok=True)  # 创建工做表
    # for i in range(len(datalist)):
    #     if i==10*k:
    #         k+=1
    #     sheet.write(i-10*(k-1),2*(k-1),datalist[i])

    k = 0
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('paqu', cell_overwrite_ok=True)  # 创建工做表
    for i in range(len(datalist)):
        if i == 10 * (k + 1):
            k += 1
        sheet.write(i - 10 * (k), 2 * (k), datalist[i])
        # if i>10:
        #     sheet.write(0,i+2,datalist[i])
        # else:sheet.write(i,0,datalist[i])
    book.save(savepath)


if __name__ == '__main__':
    main()
