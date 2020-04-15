import requests
import re
def main(page):
	'''
	param page-表示当前爬取当当网站的页数
	'''
	url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
	htmlData = requestDangDangData(url) #模拟浏览器请求当当，并且返回爬取到的数据
	result = parseHtmlData(htmlData) #对爬取到的数据进行解析

	with open('../result/book.txt','a',encoding = 'utf-8') as f:	#存数据
		for data in result:
			print(data)
			f.write('排名：'+data[0]+' '+'图片存放地址'+data[1]+' '+'书籍名称'+data[2]+' '+'评论次数'+data[3]+' '+'推荐率'+data[4]+' '+'作者：'+data[5]+'五星评分次数：'+data[6]+'\n')



def requestDangDangData(url):
	'''
	param url-请求的链接
	'''
	try:
		response = requests.get(url)#.post(url-请求的链接)
		if response.status_code == 200:
			return response.text
	except requests.RequestException:
		return None

def parseHtmlData(htmlData):
	'''
	parma htmlData 返回的数据
	'''
	#print(htmlData)
	pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
	parseData = re.findall(pattern,htmlData)

	return parseData
if __name__ == '__main__':
	for i in range(1,4):
		print(i)
		main(i)