import os ,sys
#数据集参数
path =os.path.abspath(os.path.dirname(sys.argv[0]))#当前路径
trainpath=path+'\\train\\'
testpath=path+'\\test\\'
allset_path=path+'\\话题检测数据集\\'
train_ratio=0.8
#六个分类
C4_path=allset_path+'C4-Literature\\'
C5_path=allset_path+'C5-Education\\'
C7_path=allset_path+'C7-History\\'
C17_path=allset_path+'C17-Communication\\'
C34_path=allset_path+'C34-Economy\\'
C39_path=allset_path+'C39-Sports\\'
categorys={
    'C4-':C4_path,
    'C5-':C5_path,
    'C7-':C7_path,
    'C17':C17_path,
    'C34':C34_path,
    'C39':C39_path,
}
#pyltp

LTP_DATA_DIR='D:\\codes\\python_WorkSpace\\nlp\\3.4.0\\ltp_data_v3.4.0\\ltp_data_v3.4.0'##模型路径
cws_model_path=os.path.join(LTP_DATA_DIR,'cws.model')#分词模型
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

#
corpuspath=path+'\\corpus.pickle'#仅含动词和名词
allcorpuspath=path+'\\corpusall.pickle'#包含所有词汇
testcorpuspath=path+'\\corpustest.pickle'#包含动词和名词的test语料
alltestcorpuspath=path+'\\corpusalltest.pickle'#包含所有词汇的test
modelpath=path+'\\model.pickle'
modeltest=path+'\\modeltest.pickle'
#
pylttrainvn=path+'\\pyltp分词结果\\corpus.pickle'#仅含动词和名词
pylttrainall=path+'\\pyltp分词结果\\corpusall.pickle'#包含所有词汇
pylttestvn=path+'\\pyltp分词结果\\corpustest.pickle'#包含动词和名词的test语料
pylttestall=path+'\\pyltp分词结果\\corpusalltest.pickle'#包含所有词汇的test