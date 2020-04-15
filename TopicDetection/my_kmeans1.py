import pickle
import config
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer#计数向量模块
from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.preprocessing import scale,normalize
from bikmeans import biKMeans
#训练集
trainpath=config.allcorpuspath
testpath=config.alltestcorpuspath
with open(trainpath,'rb')as f:
    model=pickle.load(f)#调用之前分好词的语料库（训练集）
sample=model['filecontent']#获取样本
print(len(model['filecontent']),'个')#输出样本个数
#根据文件名字设定分类
# #获取原始分类
filename=model['filename']
y_true=[]#原始分类数组
lendict2=[0]*6
def get_kind(filename):
    for i in range(len(filename)):
        if filename[i][:3]=='C4-':
            lendict2[0]+=1
            y_true.append(0)
        elif filename[i][:3]=='C5-':
            lendict2[1]+=1
            y_true.append(1)
        elif filename[i][:3]=='C7-':
            lendict2[2]+=1
            y_true.append(2)
        elif filename[i][:3]=='C17':
            lendict2[3]+=1
            y_true.append(3)
        elif filename[i][:3]=='C34':
            lendict2[4]+=1
            y_true.append(4)
        elif filename[i][:3]=='C39':
            lendict2[5]+=1
            y_true.append(5)
        else:
            pass
    return y_true
y_true=get_kind(filename)
# print(y_pred)
# print(y_true)
print("真实标签：",lendict2)
#TF-IDF实例化  #token_pattern保留长度为1的词
vec = TFIDF(token_pattern=r"(?u)\b\w+\b",min_df=0.05,max_df =0.7,smooth_idf=True)
X = vec.fit_transform(sample)#训练样本
array1=X.toarray()#获取数组结果
array1=normalize(array1)#正则化
#使用接口get_feature_names()调用每个列的名称 
TFIDFresult = pd.DataFrame(X.toarray(),columns=vec.get_feature_names())
# 显示
print(TFIDFresult.head())

#聚类部分
# # KMeans++
n_clusters=6#类别数量
cluster=KMeans(n_clusters=n_clusters,random_state=0).fit(array1)
y_pred=cluster.labels_#获取类别标签
# 二分聚类
# km=biKMeans(n_clusters)
# cluster1=km.fit(array1)
# y_pred=km.labels
## DBSCAN
from sklearn.cluster import DBSCAN
# dbscan=DBSCAN(eps=0.05,min_samples=5)
# y_pred=dbscan.fit_predict(array1)
# print(type(y_pred))

#画图，不同的类别使用不同的颜色
#PCA降维
from sklearn.decomposition import PCA
pca=PCA(n_components=2)
pca=pca.fit(array1)
array1=pca.transform(array1)
color=['red','green','blue','pink','orange','gray']
fig,ax1=plt.subplots(1)#构建子图
for i in range(n_clusters):
    ax1.scatter(array1[y_pred==i,0],array1[y_pred==i,1],marker='o',s=30,c=color[i])
plt.show()
# print(cluster.inertia_)簇平方误差和
#评估部分
#已知标签评估
#互信息分
info=metrics.mutual_info_score (y_pred, y_true)
#调整后的互信息分
mutual_info=metrics.adjusted_mutual_info_score (y_pred, y_true) 
#标准化互信息分
normal_info=metrics.normalized_mutual_info_score (y_pred, y_true)
print("互信息分：{0}，调整后的互信息分：{1}，标准化：{2}".format(info,mutual_info,normal_info))
 #兰德系数
lande=metrics.adjusted_rand_score(y_pred, y_true) 
print('兰德系数：',lande)
#同质性、完整性以及其调和平均
a,b,c=metrics.homogeneity_completeness_v_measure(y_true, y_pred)
print('同质性：{0}，完整性{1}，调和平均{2}'.format(a,b,c))
#未知标签评估
lunkuo=metrics.silhouette_score(array1,y_pred, metric='euclidean')#轮廓系数
print('轮廓系数：',lunkuo)
#纯度计算
from munkres import Munkres,print_matrix
from sklearn.metrics import accuracy_score



def best_map(L1,L2):#映射
	#L1是真实标签
    #L2是聚类标签
	Label1 = np.unique(L1) # 去除重复的元素，由小大大排列
	nClass1 = len(Label1) # 标签的大小
	Label2 = np.unique(L2)       
	nClass2 = len(Label2)
	nClass = np.maximum(nClass1,nClass2)#选择最大值
	G = np.zeros((nClass,nClass))#图G
    #KM算法部分：
	for i in range(nClass1):
		ind_cla1 = L1 == Label1[i]
		ind_cla1 = ind_cla1.astype(float)
		for j in range(nClass2):
			ind_cla2 = L2 == Label2[j]
			ind_cla2 = ind_cla2.astype(float)
			G[i,j] = np.sum(ind_cla2 * ind_cla1)
	m = Munkres()
	index = m.compute(-G.T)
	index = np.array(index)
	c = index[:,1]
	newL2 = np.zeros(L2.shape)
	for i in range(nClass2):
		newL2[L2 == Label2[i]] = Label1[c[i]]#映射结果
	return accuracy_score(y_true, newL2),newL2#返回纯度和映射结果
acc,y_map=best_map(y_true,y_pred)
print(acc,y_map)
ct=0
cf=0
okmap={}
rongmap={}
for i in range(len(y_pred)):
    if y_true[i]==int(y_map[i]):
        ct+=1
        okmap[y_pred[i]]=y_true[i]#获取预测标签所对应的真实标签
    
    else:
        # rongmap['t'+str(y_true[i])+'->'+str(y_map[i])]+=1
        print("错误划分{0}->{1}".format(y_true[i],y_map[i]))
        cf+=1


#预测数据——基于前面求好的质心，再放入
#预测本质和直接放入聚类是一样的#预测仅仅是减少计算量

with open(testpath,'rb')as f:
    testset=pickle.load(f)#调用之前分好词的所有测试集
sampleoftextstest=testset['filecontent']#获取样本
print('测试集共{0}个'.format(len(sampleoftextstest)))#输出样本个数

# 测试集计算TF-IDF
import nltk
from nltk.text import TextCollection
corpus = TextCollection(sample)#语料库
sample_test=[]#存储测试集所有特征向量
for j in sampleoftextstest:
    singletext=j
    words=nltk.word_tokenize(singletext) #单词列表
    tfidf_words={}
    for word in words:
        idf=corpus.idf(word)#tf
        tf=corpus.tf(word, words)#idf
        tfidf=idf*tf
        tfidf_words[word]=tfidf
    #根据语料库词特征构建词向量
    test_tfvec=[]
    # 对于每个特征词
    for i in list(vec.get_feature_names()):
        
        if i not in tfidf_words.keys():
            test_tfvec.append(0.)#不存在设置为0
        else:
            test_tfvec.append(tfidf_words[i])
    sample_test.append(test_tfvec)
sample_test=np.array(sample_test)
# 获取质心
centroid = cluster.cluster_centers_ 
result=[]


for i in sample_test:
    resulti=[]
    for c in centroid:
        #计算测试点到质心的距离
        vecA=i
        vecB=c
        resulti.append(np.linalg.norm(vecA - vecB))
    result.append(resulti.index(min(resulti)))
    print(resulti)
    resulti2=resulti
    resulti2.sort()#排序
    print(resulti2)
    #根据最近距离选出所属簇的质心

    
y_testpred=result#预测值

y_testtrue=get_kind(testset['filename'])[120:]

countok=0
for i in range(len(y_testpred)):
    if int(okmap[y_testpred[i]])==int(y_testtrue[i]):
        countok+=1
print('测试集准确率：',1-countok/len(y_testpred))
#二分kmeans预测
#

# pre = km.predict(sampletest)
# DBSCAN预测
# testX = vec.fit_transform(sampletest)#训练样本
# array2=testX.toarray()#获取数组结果
# array2=normalize(array2)#正则化
# pre = dbscan.fit_predict(array2)





