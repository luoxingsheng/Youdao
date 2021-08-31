# 爬虫基础包
import requests
# json处理包
import json

# 中文翻英文或英文翻中文
def translation(content):
	# 和官网的链接不算同一个，需要去掉_o
	url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
	headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
	# 请求表单必须字段
	form_data={
		"i": content,
		"from": "AUTO",
		"to": "AUTO",
		"doctype": "json"
	}
	response = requests.post(url, data=form_data, headers=headers)
	response.encoding = "utf-8"
	html_str = response.content
	dict_str = json.loads(html_str)
	query = dict_str['translateResult'][0][0]['src']
	result = dict_str['translateResult'][0][0]['tgt']
	print("查询字段：",query)
	print("结果：",result)

def main():
	while True:
		content = input("请输入要翻译的文本：")
		translation(content)

if __name__ == '__main__':
	main()