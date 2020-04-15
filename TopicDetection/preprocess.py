import main
import config
import os
from pyltp import Segmentor,Postagger
from config import cws_model_path,pos_model_path
from init_set import whereisfile,init_testfiles,getfilename_ofinit
# import sklearn
import pickle

# from sklearn.externals import joblib #joblib是sklearn的一个外部模块,保存模型用




def readfile(filename,dirpath):#根据文件名,和文件所在路径获取文件内容
    with open(dirpath+filename,'r',encoding='utf-8') as f:#utf-8
        lines=f.readlines()

    content_str=' '.join(lines)
    return content_str

def segmentor_str(str):
    ##分词
    #输入参数为字符串
    #得到单词列表
    segmentor=Segmentor()
    segmentor.load(cws_model_path)
    words=segmentor.segment(str)
    # print(type(words))#<class 'pyltp.VectorOfString'># print('\t'.join(words))
    segmentor.release()#释放模型
    return list(words)



def get_postager(wordslist,poslist):
    #获得名词和动词，输入为分词结果(单词列表)，
    # 和需要的属性名称的列表，
    # 输出为相应词的单词列表
    
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(wordslist)  # 词性标注
    # print('\t'.join(postags))
    
    newlist=[]
    for a in poslist:
        for i in range(len(list(postags))):
            if list(postags)[i][0]==a:#元素类型为str
                newlist.append(wordslist[i])
    postagger.release()  # 释放模型
    return newlist
import jieba
def get_allfile_content(filelist,path,posts):#posts为可以设定的词性列表
    #根据posts筛选出需要的某些词性的词语
    allf_content=[]#所有文件的分词结果 类型：list of str
    #pyltp
    segmentor=Segmentor()# # 初始化分词模型实例
    segmentor.load(cws_model_path)#根据地址加载模型
    if posts!=[]:#如果词性列表不为空
        postagger = Postagger() # 初始化词性标注模型实例
        postagger.load(pos_model_path)  # 加载模型
    count=0#计数
    for i in filelist:#i为单个文件名
        punctuations = """,，.。：…・《》［］～[]【】－－〈〉―()②③④⑤⑥⑦⑧⑨⑩①①①②①④①⑦（）/~*&^%$#@＠！“”‘；~`[]{|、}\\/\n\t\r~+_-=？"""
        digit='01234567897一二三四五六七八九０１２３４５６７８９'
        alpha='ａabcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        punctuations+=digit
        punctuations+=alpha
        content=readfile(i,path)
        for punc in punctuations:#去标点符号和特殊符号、数字
            content=content.replace(punc,' ')
        words=list(segmentor.segment(content))#分词
        
        
        if posts!=[]:
            postags = postagger.postag(words)  # 词性标注
            #选择需要的词性
            newlist=[]
            for a in posts:
                for i in range(len(list(postags))):
                    if list(postags)[i][0]==a:#元素类型为str
                        newlist.append(words[i])
        else:#不筛选词性
            newlist=words
        contentoffile=' '.join(newlist)#结果连接为字符串
        allf_content.append(contentoffile)
        print(count)#进度显示
        count+=1
    segmentor.release()#释放模型   
    if posts!=[]:
        postagger.release()  # 释放模型
    return allf_content

def norepeat(wordslist):
    allwords=[]
    for i in wordslist:
        if  i not in allwords:
            allwords.append(i) 
    return allwords

if __name__ == "__main__":
    trainlist,testlist=getfilename_ofinit()
    # print(testlist)
    #test动词名词
    # allcontentsoftest=get_allfile_content(testlist[:],config.testpath,['v','n'])#['v','n']
    #test所有词汇
    allcontentsoftest=get_allfile_content(testlist[:],config.testpath,[])#['v','n']
    #train所有词汇
    allcontentsoftrain=get_allfile_content(trainlist[:],config.trainpath,[])
    #train动词名词
    # allcontentsoftrain=get_allfile_content(trainlist[:],config.trainpath,['v','n'])
    

    trainmodel={}
    trainmodel['filename']=trainlist
    trainmodel['filecontent']=allcontentsoftrain

    testmodel={}
    testmodel['filename']=testlist
    testmodel['filecontent']=allcontentsoftest
    
    
    # with open(config.corpuspath,'wb')as f: 
    #     pickle.dump(trainmodel,f) #将模型dump进f里面
    with open(config.allcorpuspath,'wb')as f: 
        pickle.dump(trainmodel,f) #将模型dump进f里面
    # with open(config.testcorpuspath,'wb')as f: 
        # pickle.dump(testmodel,f) #将模型dump进f里面
    with open(config.alltestcorpuspath,'wb')as f:
        pickle.dump(testmodel,f) #将模型dump进f里面