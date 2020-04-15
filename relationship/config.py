from mytools import getthisdirpath,converformat
path=getthisdirpath() 
class NamePeople(object):
    
    def __init__(self):
        #转化编码
        self.peoplepath=path+"\\人民的名义材料\\people.txt"
        self.juqingpath=path+"\\人民的名义材料\\剧情梗概.txt"
        
        self.stopwords=['吕州','林城','银行卡','明白','白云','嗡嗡嘤嘤',
           '阴云密布','雷声','陈大','谢谢您','安置费','任重道远',
           '孤鹰岭','阿庆嫂','岳飞','师生','养老院','段子','老总']
        self.replacewords={'师母':'吴慧芬','陈老':'陈岩石','老赵':'赵德汉','达康':'李达康','高总':'高小琴',
              '猴子':'侯亮平','老郑':'郑西坡','小艾':'钟小艾','老师':'高育良','同伟':'祁同伟',
              '赵公子':'赵瑞龙','郑乾':'郑胜利','孙书记':'孙连城','赵总':'赵瑞龙','昌明':'季昌明',
               '沙书记':'沙瑞金','郑董':'郑胜利','宝宝':'张宝宝','小高':'高小凤','老高':'高育良',
               '伯仲':'杜伯仲','老杜':'杜伯仲','老肖':'肖钢玉','刘总':'刘新建',"美女老总":"高小琴"}
        self.edgepath=path+"\\边文件\\NamePeople_edge.csv"
        converformat(self.peoplepath,'gb2312')
        converformat(self.juqingpath,"gb2312")

class RedDream(object):
    
    def __init__(self):
        #转化编码
        self.peoplepath=path+"\\红楼梦材料\\people.txt"
        self.juqingpath=path+"\\红楼梦材料\\剧情梗概.txt"
        #这部分较少
        self.stopwords=['明白']
        self.replacewords={'宝玉':'贾宝玉','黛玉':'林黛玉','林妹妹':'林黛玉',"宝钗":"薛宝钗"}
        self.edgepath=path+"\\边文件\\RedDream_edge.csv"
        converformat(self.peoplepath,'gb2312')
        converformat(self.juqingpath,"gb2312")