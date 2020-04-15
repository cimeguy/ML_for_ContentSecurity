# 代码部分

- init_set.py初始化选择训练集、测试集，获取文件名等    
- preprocess.py预处理：分词、筛选词性
- my_kmeans1.py使用kmeans++流程+评估
- my_kmeans2.py使用二分kmeans流程+评估
- bikmeans.py为kmeans类和二分kmeans类
- 所有.pickle文件都是中间生成的模型，直接在源码中调用
- 此外，给出了分词和筛选好词性的全部预料的模型、pyltp的分词好的模型
- test为测试集
- train训练集
- 话题检测数据集为所有数据集

# 环境问题
## 安装pyltp  
注意网上只有支持python3.6和3.5的版本
这里安装的是python3.7版本 
1. 下载轮子 网址：https://download.csdn.net/download/grove_ai/11750723?depth_1-utm_source=distribute.pc_relevant.none-task-download-BlogCommendFromMachineLearnPai2-1&utm_source=distribute.pc_relevant.none-task-download-BlogCommendFromMachineLearnPai2-1
2. 放入Scripts文件夹中，我这里是`D:\soft\Anaconda3\envs\python37\Scripts`
3. cmd打开：`pip install pyltp-0.2.1-cp37-cp37m-win_amd64.whl`
4. 下载模型：网址： https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2F       
   下载最新的3.4.0即可，随便放入一个文件夹，win下解压`ltp_data_v3.4.0.zip`       
   后续使用只需直接引用这个文件夹位置即可

## numpy问题
之前安装的numpy突然出现问题：
``` dotnetcli
Note: this error has many possible causes, so please don't comment on
an existing issue about this - open a new one instead.

Original error was: DLL load failed: 找不到指定的模块。
```
解决方法：`conda install numpy-base`


