#coding=utf-8
# 爬虫基础包
import requests
#引入json字符串处理模块
import json
# hash
import hashlib
# 随机数
import random
# 时间
import time

# 中文翻英文或英文翻中文
def translation(content,from_,to_):
    # url和官网一致，此url请求的参数经过多层封装和校验
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # headers必须的参数
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://fanyi.youdao.com/',
        'Cookie': 'OUTFOX_SEARCH_USER_ID="-1848382357@10.169.0.84"; ___rl__test__cookies=1625907853887; OUTFOX_SEARCH_USER_ID_NCOO=132978720.55854891'
    }
    # 加密参数的方法，需要去翻js
    lts = str(int(time.time() * 1000))  # 以毫秒为单位的 13 位时间戳
    salt = lts + str(random.randint(0, 10))  # 13 位时间戳+随机数字，生成 salt 值
    sign = "fanyideskweb" + content + salt + "Y2FYu%TNSbMCxc3t2u^XT"  # 拼接字符串组成 sign
    sign = hashlib.md5(sign.encode()).hexdigest()  # 将 sign 进行 MD5 加密，生成最终 sign 值
    bv = hashlib.md5(user_agent.encode()).hexdigest()  # 对 UA 进行 MD5 加密，生成 bv 值
    form_data={
    "i": content,
    "from": from_,
    "to": to_,
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": salt,
    "sign": sign,
    "lts": lts,
    "bv": bv,
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTlME",
    }
    response = requests.post(url, data=form_data, headers=headers)
    response.encoding = "utf-8"
    html_str = response.content
    dict_str = json.loads(html_str)
    # print(dict_str)
    # 一些文本不能正确翻译，做特殊处理否则报错
    if (dict_str['errorCode'] == 40):
        print("输入的文本不能识别，请重试")
    else:
        query = dict_str['translateResult'][0][0]['src']
        result = dict_str['translateResult'][0][0]['tgt']
        print("查询字段：",query)
        print("结果：",result)
        # 一些翻译没有关联信息，需要做特殊处理，否则报错
        if "smartResult" in dict_str:
            list1 = dict_str['smartResult']['entries']
            list2 = []
            # 去掉空格
            for item in list1:
                if item:
                    list2.append(item.strip())
            smartResult = ",".join(list2)
            print("关联信息：",smartResult)
        else:
            print("无关联信息")

# 手动选择翻译方式
def check_method(checkd_value):
    # 自动识别
    if (checkd_value == "0"):
        from_ = "AUTO"
        to_ = "AUTO"
    # 中文翻英文
    elif (checkd_value == "1"):
        from_ = "zh-CHS"
        to_ = "en"
    # 英文翻中文
    elif (checkd_value == "2"):
        from_ = "en"
        to_ = "zh-CHS"
    # 中文翻韩文
    elif (checkd_value == "3"):
        from_ = "zh-CHS"
        to_ = "ko"
    # 韩文转中文
    elif (checkd_value == "4"):
        from_ = "ko"
        to_ = "zh-CHS"
    # 中文转日文
    elif (checkd_value == "5"):
        from_ = "zh-CHS"
        to_ = "ja"
    # 日文转中文
    elif (checkd_value == "6"):
        from_ = "ja"
        to_ = "zh-CHS"
    else:
        print("输入有误，请检查")
        from_ = "error"
        to_ = "error"
    return from_,to_

# 展示选择方式
def show_check():
    print("""
0: 自动识别
1： 中文转英文
2： 英文转中文
3： 中文转韩文
4： 韩文转中文
5： 中文转日文
6： 日文转中文
            """)

def main():
    while True:
        show_check()
        check_value = input("请选择翻译方式：")
        from_, to_ = check_method(check_value)
        # 如果输入方式有误，不进行翻译
        if (from_=="error" or to_=="error"):
            continue
        content = input("请输入要翻译的文本：")
        translation(content,from_,to_)

if __name__ == '__main__':
    main()

