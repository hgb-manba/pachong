#-*- codeing= utf-8 -*-
#@Time :2021/2/3 19:09
#@Author:
#@File:spider.py
#@Software:PyCharm

from bs4 import BeautifulSoup
#网页解析，获取数据
import  re #正则表达式，进行文字匹配
import  urllib.request,urllib.error #制定url，获取网页数据
import xlwt   #excel操作
import sqlite3   #进行sqlite数据库操作

def main():
    baseurl="https://movie.douban.com/top250?start="
    #1爬取网页
    datalist=getDate(baseurl)
    savepath=".\\豆瓣电影TOP250.xls"#当前路径
    # 3保存数据
    saveDate(datalist,savepath)
    #askURL("https://movie.douban.com/top250?start=")


findLink=re.compile(r'<a href="(.*?)">')#创建正则表达式对象，表示规则
#图
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)#创建正则表达式对象，表示规则
#标题
findTitle=re.compile(r'<span class="title">(.*)</span>')
#评分
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge=re.compile( r'<span>(\d*)人评价</span>')
#找到概况
findInq=re.compile(r'<span class="inq">(.*)</span>')
#找到影片相关内容
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)#忽视换行符re.s

def getDate(baseurl):
    datalist = []
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askURL(url)
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data=[]
            item=str(item)


            link=re.findall(findLink,item)[0]
            data.append(link)


            imgSrc=re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            titles=re.findall(findTitle,item)
            if(len(titles)==2):
                ctitle=titles[0]
                data.append(ctitle)
                otitle=titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles)
                data.append(' ')#外国名字留空

            rating=re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum=re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq=re.findall(findInq,item)#判断有没有
            if len(inq)!=0:
                inq=inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?'," ",bd)#去掉bd
            # bd.re.sub('/'," ",bd)#替换/ .出错
            bd=re.sub('/'," ",bd)
            data.append(bd.strip())#去掉前后的开个空格

            datalist.append(data)#处理好的一部电影信息放入datalist

    print(type(datalist))
    return datalist

#1.1获取网页源码
def askURL(url):
    head={#模拟头部信息
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
          }
   #用户代理告诉豆瓣服务器，我们是什么类型的浏览器
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
       response=urllib.request.urlopen(request)
       html=response.read().decode("utf-8")
       #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if  hasattr(e,"reason"):
            print(e,"reason")
    return html#!!!return 有一个缩进错误



def saveDate(datalist,savepath):

    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影250',cell_overwrite_ok=True)  # 创建工做表
    col=("电影详情链接","图片链接","影片中文名","影片外国名","评分","评分数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d"%(i+1))
        data=datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])


    book.save(savepath)



if __name__ == '__main__':
    main()
    print("爬取成功")