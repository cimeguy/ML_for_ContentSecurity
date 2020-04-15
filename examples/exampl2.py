#request 获取网页源码
#beautifulsoup对内容进行解析
#将解析好的内容存在excel文件里面，写入excel文件； xlrt 读取excel文件

from bs4 import BeautifulSoup as bs 
import requests
import xlwt 

workbook = xlwt.Workbook(encoding='utf-8') ## 创建一个workbook并且设置编码
worksheet = workbook.add_sheet('DangDangBook Top 60')#创建一个表格，命名为“DangDangBook Top 100”
worksheet.write(0,0,'书籍排名')#第一个参数行 第二个列
worksheet.write(0,1,'书籍名称')
worksheet.write(0,2,'书籍作者')
worksheet.write(0,3,'书籍五星评分次数')
worksheet.write(0,4,'书籍价格')
row = 1
def main(pages):
	url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'+str(pages)
	print(pages)
	html = reuqestDangDangData(url)
	#print(html)
	soup = bs(html,'lxml')
	lists = soup.find(class_='bang_list clearfix bang_list_mode').find_all('li')
	#print(lists)

	global row
	for each in lists:
		#print(each)
		eachBookindex = (each.find(class_='list_num').string).strip('.')
		eachPicAd = each.find(class_='pic').find('img').get('src') #get方法获取<>内内容
		eachBookName = each.find(class_='name').find('a').get('title')
		eachBookIntrNum = each.find(class_='star').find('a').string
		eachBookIntrPer = each.find(class_='star').find(class_='tuijian').string
		eachBookAuthor = each.find(class_='publisher_info').find('a').string
		eachBookFiveStarNum = each.find(class_='biaosheng').find('span').string
		eachBookPrice = each.find(class_='price').find(class_='price_n').string

		print('书籍排名：'+eachBookindex+'|'+'书籍名称：'+eachBookName+'|'+'书籍作者：'+eachBookAuthor+'|'+'书籍五星评分次数：'+eachBookIntrNum+'|'+'书籍价格：'+eachBookPrice)
		print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
		worksheet.write(row,0,eachBookindex)
		worksheet.write(row,1,eachBookName)
		worksheet.write(row,2,eachBookAuthor)
		worksheet.write(row,3,eachBookIntrNum)
		worksheet.write(row,4,eachBookPrice)

		row = row + 1 

def reuqestDangDangData(url):
	try:
		response = requests.get(url)
		#print(response.status_code)
		if response.status_code == 200:
			return response.text
	except requests.RequestException:
		return None 

if __name__ == '__main__':
	for i in range(1,4):
		main(i)
	workbook.save('../result/book2.xls')