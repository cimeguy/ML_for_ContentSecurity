import os ,sys
import random

from config import train_ratio
import config
import shutil
import chardet
import os
# import convertformat as cf
trainnametext=config.trainpath+'\\训练集文件说明.txt'
testnametext=config.testpath+'\\测试集文件说明.txt'
#编码转换
def converformat(file,queshengcode):#第二个参数为缺省编码，有的文件解析编码为None，解码时则使用缺省编码
    filename=os.path.splitext(file)
    # print(('convert{0}.{1}').format(filename[0],filename[1]))
    with open (file,'rb+')as f:
        content=f.read()
        encode=chardet.detect(content)['encoding']
        print(file,encode)

        if(encode!='utf-8'):
            try:
                if encode==None:#如果编码缺了，则改成缺省编码
                     encode=queshengcode
                gbk_content=content.decode(encode,'ignore')#如果设置为ignore，则会忽略非法字符； 
                #如果设置为replace，则会用?号取代非法字符； 
                utf_byte=bytes(gbk_content,encoding='utf-8')
                f.seek(0)
                f.write(utf_byte)
            except IOError:
                print('fail')


#使用：convertDir(config.C4_path)
def convertDir(dirpath):
    
    print('====================编码转化=======================')
    for file in os.listdir(dirpath):
        file = os.path.join(dirpath,file)
        converformat(file,'GB2312')

def get_trainandtest_random(filelist):#输入文件名列表，按照设定值随机选择测试和训练集
    trainnum=20
    testnum=18
    train_list=random.sample(filelist,trainnum)
    # print("文件总数{0}".format(len(filelist)))
    # print("训练集数{0}".format(len(train_list)))
    # print(len(train_list))
    shenyu=[]#其余随机作为测试集
    for i in filelist:
        if i not in train_list:
            shenyu.append(i)  
    # print(len(shenyu))
    if len(shenyu)<testnum:
        testnum=len(shenyu)
    else:
        pass
    test_list=random.sample(shenyu,6) 
    # print('剩余',len(shenyu))
    # print('test',len(test_list))

    return train_list,test_list

def init_testfiles(move=False):
    #初始化，按照设定比率，随机选择测试集和训练集

    #获得所有数据集文本名
    C4filenameslist=getfiles(config.C4_path)
    C5filenameslist=getfiles(config.C5_path)
    C7filenameslist=getfiles(config.C7_path)
    C17filenameslist=getfiles(config.C17_path)
    C34filenameslist=getfiles(config.C34_path)
    C39filenameslist=getfiles(config.C39_path)
    lenall=len(C4filenameslist)+len(C5filenameslist)+len(C7filenameslist)+len(C17filenameslist)+len(C34filenameslist)+len(C39filenameslist)
    print(len(C34filenameslist))
    #随机选择训练、测试集
    C4train,C4test=get_trainandtest_random(C4filenameslist)
    C5train,C5test=get_trainandtest_random(C5filenameslist)
    C7train,C7test=get_trainandtest_random(C7filenameslist)
    C17train,C17test=get_trainandtest_random(C17filenameslist)
    C34train,C34test=get_trainandtest_random(C34filenameslist)
    C39train,C39test=get_trainandtest_random(C39filenameslist)
    #把所有测试集、训练集分别放在一起
    alltrainsetlist=[]
    alltrainsetlist.extend(C4train)
    alltrainsetlist.extend(C5train)
    alltrainsetlist.extend(C7train)
    alltrainsetlist.extend(C17train)
    alltrainsetlist.extend(C34train)
    alltrainsetlist.extend(C39train)
    alltestsetlist=[]
    alltestsetlist.extend(C4test)
    alltestsetlist.extend(C5test)
    alltestsetlist.extend(C7test)
    alltestsetlist.extend(C17test)
    alltestsetlist.extend(C34test)
    alltestsetlist.extend(C39test)
    print('总共{0}个文件，训练集有{1}个，测试集有{2}个'.format(lenall,len(alltrainsetlist),len(alltestsetlist)))
    #清空之前运行时暂时存储测试集训练集的文件夹
    
    RecreateDir(config.trainpath)
    RecreateDir(config.testpath)
    print('训练集比率为{0}'.format(len(alltrainsetlist)/lenall))
    if move:

        for f in alltrainsetlist:
           
            movefiles(config.trainpath,[f],whereisfile(f))
        for t in alltestsetlist:
            movefiles(config.testpath,[t],whereisfile(t))
    print('初始化成功，测试集在test中，训练集在train中')
    with open (trainnametext,'w')as f1:
        # f1.write("训练集包括以下文件:\n")
        f1.write('\t'.join(alltrainsetlist))
    with open (testnametext,'w')as f2:
        # f2.write("测试集集包括以下文件:\n")
        f2.write('\t'.join(alltestsetlist))
    return alltrainsetlist,alltestsetlist
#找出文件名（不包括目录）所在目录
def whereisfile(filename):
    pre=filename[0:3]
    for k in config.categorys.keys():
        if pre==k:
            path=config.categorys[k]
    return path




# 使用：C4filenameslist=getfiles(config.C4_path)
def getfiles(path):#获取某个目录（文件夹）下所有文件名，返回文件名列表
    fileslist=[]
    for root, dirs, files in os.walk(path):  #目录路径
        
        for file in files:
            fileslist.append(file)
    return fileslist

def RecreateDir(dirpath):#重新创建文件夹 用于划分测试集和训练集用

    if os.path.exists(dirpath):  # 如果文件夹存在
        shutil.rmtree(dirpath)    #递归删除文件夹
        os.makedirs(dirpath)#并创建新文件夹
    else:#否则创建新文件夹
        os.makedirs(dirpath)
        
def movefiles(destdir,pathlists,srcdir):#批量复制文件到另外的目录，pathlists是文件名，不包含目录
    srcpath=''
    destpath=''
    for path in pathlists:
        srcpath=srcdir+path
        
        destpath=destdir+path
        shutil.copyfile(srcpath,destpath)

def getfilename_ofinit():
    with open(trainnametext,'r') as f:
        lines=f.readlines()
    strlines=''.join(lines)
    trainlist=strlines.split('\t')
    print('训练集：',len(trainlist))
    # print(trainlist)
    with open(testnametext,'r') as f:
        lines=f.readlines()
    strlines=''.join(lines)
    testlist=strlines.split('\t')
    print('测试集',len(testlist))
    return trainlist,testlist

if __name__ == "__main__":
    ##编码转化为UTF-8
    # convertDir(config.C4_path)
    # convertDir(config.C5_path)
    # convertDir(config.C7_path)
    # convertDir(config.C17_path)
    # convertDir(config.C34_path)
    # convertDir(config.C39_path)
    #初始化训练集和测试集，并挪入train和test中
    init_testfiles(True)#True表示将文件移动至train和test中
    # getfilename_ofinit()#从说明文件中帮助读取train和test文件名
