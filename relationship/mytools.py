
import os,sys,chardet
#获取当前文件夹路径
def getthisdirpath():
    
    path =os.path.abspath(os.path.dirname(sys.argv[0]))#当前路径
    return path

#转换文件夹内所有文件的编码
#使用：convertDir(config.C4_path)
def convertDir(dirpath,queshengcode='gb2312'):
    
    print('====================编码转化=======================')
    for file in os.listdir(dirpath):
        file = os.path.join(dirpath,file)
        converformat(file,queshengcode)

#单个文件编码转换
# 例如converformat(file,'GB2312')
def converformat(filename,queshengcode="gb2312"):#第二个参数为缺省编码，有的文件解析编码为None，解码时则使用缺省编码
    file=filename
    filename=os.path.splitext(file)
    # print(('convert{0}.{1}').format(filename[0],filename[1]))
    with open (file,'rb+')as f:
        content=f.read()
        encode=chardet.detect(content)['encoding']
        print("文件{0}原编码为：{1}".format(file,encode))

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
    

