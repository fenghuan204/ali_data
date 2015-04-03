# -*- coding: cp936 -*-
'''
#author: SomeOne
#date: 2015-04-02
#copyright: default
'''
import urllib2
from bs4 import BeautifulSoup
import re
import os.path
import csv
import sys, codecs

def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
   
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)

def jd(url, filename):
    page = urllib2.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc.decode('utf-8','ignore'))
    aa = soup.findAll('li', class_='list-item')
    for i in aa:
        drank = i.find('div', class_='ranking')
        prank = drank.find('p')
        srank = re.findall(r'[0-9]{1,3}',str(prank))
        size = len(srank)
        chg = ''
        if(size>1):
            if prank.find('span', class_='down'):
                #chg = '↓'
                chg = 'D'
            else:
                #chg = '↑'
                chg = 'U'
        

        member = i.find('div', class_='member-box')
        team_name = member.find('p')
        team_name="".join(filter_tags(str(team_name)).split())
        
        school = i.find('div', class_='team-box')
        school = school.find('p')
        school="".join(filter_tags(str(school)).split())
        
        f1score = i.find('div', class_='score')
        f1score="".join(filter_tags(str(f1score)).split())
        
        accuracy = i.find('div', class_='rate-accuracy')
        accuracy="".join(filter_tags(str(accuracy)).split())
        
        recall = i.find('div', class_='rate-recall')
        recall="".join(filter_tags(str(recall)).split())
        
        best_time = i.find('div', class_='best-time')
        best_time="".join(filter_tags(str(best_time)).split())
        
        
        tarr = [srank[0], team_name, school, f1score, accuracy, recall, best_time]
        if(chg):
            tarr.append(chg+" "+srank[1])

        
        #ss = ",".join(tarr)
        filename.writerow(tarr)

if __name__ == "__main__": 
    output = open("F:/result.csv", "wb")
    output.write(codecs.BOM_UTF8)
    ww = csv.writer(output, dialect='excel')   
    tarr = ["Rank", "TeamName", "School", "F1Score", \
            "Accuracy", "Recall", "BestTime", "Change"]
    #ss = ",".join(tarr)
    ww.writerow(tarr)
    for i in range(1,26):
        url = "http://tianchi.aliyun.com/competition/"+\
           "rankingList.htm?season=0&raceId=1&pageIndex="+str(i)
        jd(url, ww)
    output.close()
