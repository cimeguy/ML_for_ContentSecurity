# -*- encoding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import codecs
import csv
from config import NamePeople,RedDream
from mytools import converformat,getthisdirpath
import networkx as nx

G=NamePeople()
G=RedDream()
stopwords=G.stopwords
replace_words=G.replacewords
juqingpath=G.juqingpath
peoplepath=G.peoplepath
path=getthisdirpath()
names={} #所有人物
relationships ={} #关系
lineNames =[] #每段人物
node=[] #存放处理后的人物/节点

def read_txt(path): #处理部分
    
    jieba.load_userdict(G.peoplepath) #加载所有人物
    #读取剧情
    with open (path,"r",encoding="utf-8") as f:
        lines=f.readlines()
    #对于每一段，分词、去停用词，得到词性，筛选人物名称
    for line in lines:
        poss=pseg.cut(line) 
        lineNames.append([]) 
        for w in poss:
            if w.word in stopwords: 
                continue
            if w.flag != "nr" or len(w.word) <2 : 
                if w.word not in replace_words: 
                    continue
            if w.word in replace_words: #将特殊称呼替换为正式名字
                w.word=replace_words[w.word]
            lineNames[-1].append(w.word)  #为当前段增加一个人物
            if names.get(w.word) is None: #如果这个名字从来没出现过，添加关系
                names[w.word] =0
                relationships[w.word] ={}
            names[w.word] +=1 #该人物出现次数加1
    #得到所有边
    for line in lineNames: 
        for name1 in line:
            for name2 in line:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None: #之前没有这个关系
                    relationships[name1][name2] =1
                else:
                    relationships[name1][name2] +=1 #有关系
def write_csv():
    #写入边文件
    csv_edge_file = open(G.edgepath, "w", newline="")
    writer = csv.writer(csv_edge_file)
    #第一行
    writer.writerow(["source", "target", "weight","type"])  
    for name,edges in relationships.items():
        for v,w in edges.items():
            if w>20:
                node.append(name)
                #无向图
                writer.writerow((name,v,str(w),"undirected"))  
    csv_edge_file.close()
    

if __name__=='__main__':
    #读取内容
    read_txt(juqingpath)
    #输出边
    write_csv()
