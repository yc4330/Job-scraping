import requests
import pdb
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json
#{'code': 430, 'message': '签名错误', 'askId': 'b4c377fdb50d0947bc05339a00b6328b', 'data': None, 'error': True}
# storage_state_file = "yupao_account.json"

# def intercept_request(route):
#     # 获取请求头 https://yupao-prod.yupaowang.com/job/v2/search/job/pc/search
#     request=route.request
#     print(request.url)
#     # if request.url=="https://yupao-prod.yupaowang.com/job/v2/search/job/pc/search":
#     #     print(request.url)
#     headers = request.headers
#     # 检查是否存在 sign 字段
#     if 'Sign' in headers:
#         print(f"截获到的 time 值: {headers['Timestamp']}")
#         print(f"截获到的 sign 值: {headers['Sign']}")
#     return route.continue_()

# def scrape_jobs():
#     file = open('搜索关键词_boss.txt', 'r', encoding='utf-8')
#     # 读取文件内容
#     search_key_boss = file.read()
#     # 关闭文件
#     file.close()
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--mute-audio"])
#         # 尝试加载已保存的登录状态
#         if os.path.exists(storage_state_file):
#             context = browser.new_context(storage_state=storage_state_file)
#             print("加载已保存的登录信息...")
#             page = context.new_page()
#             page.route('**/*yupaowang*', intercept_request)
#             # pdb.set_trace()
#             page.goto("https://www.yupao.com/topic/a2c0/?keywords="+str(search_key_boss))
#             while True:
#                 pass
#         # 关闭浏览器
#         browser.close()

# # 运行抓取任务
# scrape_jobs()

def get_detail(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "areaInfo=%7B%22id%22%3A2%2C%22pid%22%3A1%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22nameA%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22ltr%22%3A%22beijing%22%2C%22lv%22%3A1%2C%22adcode%22%3A%22110000%22%7D; areaInfo=%7B%22id%22%3A2%2C%22pid%22%3A1%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22nameA%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22ltr%22%3A%22beijing%22%2C%22lv%22%3A1%2C%22adcode%22%3A%22110000%22%7D; gt_local_id=vOHFGLllL2Hv1ZyFdPBovPFIoNywlOGu38avfKSA3wHd2a1UuNMIwA==; DEVICEID=%22GEE3-01-abb62e88c6b4ef4a89ff73726b7b64204043ec8d9b7749c07763050e723186a5%22; DEVICEID=%22GEE3-01-abb62e88c6b4ef4a89ff73726b7b64204043ec8d9b7749c07763050e723186a5%22",
        "Referer": "https://www.yupao.com/topic/a2c0/?keywords=%E6%99%AE%E5%B7%A5",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')
        if script_tag:
            # 获取 script 标签中的 JSON 字符串
            json_data = script_tag.string

            # 将 JSON 字符串解析为 Python 字典
            data = json.loads(json_data)
            gongsimingcheng=data['props']['pageProps']['ppQiYeInfo']['name']
            # 打印解析后的数据
            return gongsimingcheng
        else:
            print("未找到 <script id='__NEXT_DATA__'> 标签")
            return ''
    except Exception as e:
        return ''

for page_index in range(1,100):

    # url = "https://yupao-prod.yupaowang.com/job/v2/search/job/pc/search"

    # headers = {
    #     "Accept": "application/json, text/plain, */*",
    #     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    #     "Connection": "keep-alive",
    #     "Content-Type": "application/json",
    #     "Origin": "https://www.yupao.com",
    #     "Referer": "https://www.yupao.com/topic/a2c0/?keywords=%E6%99%AE%E5%B7%A5",
    #     "Sec-Fetch-Dest": "empty",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Site": "cross-site",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    #     "business": "YPZP",
    #     "hybird": "NO",
    #     "nonce": "864014",
    #     "os": "WINDOWS",
    #     "osversion": "10",
    #     "packagename": "yp.pc",
    #     "packageversion": "8.1.0",
    #     "reqsource": "YPZP",
    #     "request-source": "java",
    #     "runtime": "PC",
    #     "runtimeversion": "132.0.0.0",
    #     "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Microsoft Edge\";v=\"132\"",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": "\"Windows\"",
    #     "sign": "399716cc6ecc2b8fe9b4405be6ba254b8197ccb394e11e866fcd4e172e341ef7",
    #     "signVersion": "1",
    #     "timestamp": "1739428147640",
    #     "token": ""
    # }

    # data = {
    #     "keywords": "普工",
    #     "token": "",
    #     "currentPage": page_index,
    #     "pageSize": 36,
    #     "areaIds": ["2"],
    #     "occV2": [],
    #     "filterCondition": {}
    # }
    url = "https://www.yupao.com/topic/a2c0/?keywords=%E6%99%AE%E5%B7%A5"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "areaInfo=%7B%22id%22%3A2%2C%22pid%22%3A1%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22nameA%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22ltr%22%3A%22beijing%22%2C%22lv%22%3A1%2C%22adcode%22%3A%22110000%22%7D; areaInfo=%7B%22id%22%3A2%2C%22pid%22%3A1%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22nameA%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22ltr%22%3A%22beijing%22%2C%22lv%22%3A1%2C%22adcode%22%3A%22110000%22%7D; gt_local_id=vOHFGLllL2Hv1ZyFdPBovPFIoNywlOGu38avfKSA3wHd2a1UuNMIwA==; DEVICEID=%22GEE3-01-abb62e88c6b4ef4a89ff73726b7b64204043ec8d9b7749c07763050e723186a5%22; DEVICEID=%22GEE3-01-abb62e88c6b4ef4a89ff73726b7b64204043ec8d9b7749c07763050e723186a5%22",
        "Referer": "https://www.yupao.com/a2/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    response = requests.get(url, headers=headers)
    try:
        # response = requests.post(url, headers=headers, json=data)
        # data_list = response.json()['data']['list']
        response.raise_for_status()  # 检查响应状态码，如果不是 200 会抛出异常
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')
        # 获取 script 标签中的 JSON 字符串
        json_data = script_tag.string
        data_list = json.loads(json_data)['props']['pageProps']['pageData']['jobList']
        
        # CSV文件的列名
        fieldnames = ['具体地点', '职位名称', '工资', '福利tag', '公司名称', '公司标签', '其他标签', '岗位要求', '是否为推广', '会员商家', '发布时间', '抓取时间']
        existing_data = []
        with open('jobs_yupao.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
        # 打开CSV文件，如果文件存在则追加数据，否则创建新文件
        with open('jobs_yupao.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # 如果文件为空，写入表头
            writer.writeheader()
            
            for data in data_list:
                # jobId = data['jobId']
                # detail_url = "https://www.yupao.com/zhaogong/" + str(jobId) + ".html"
                # gongsimingcheng = get_detail(detail_url)
                # jutididian = data['address']
                # zhiweimingcheng = data['title']
                # qitabiaoqian = data['detail']
                # fabushijian = data['updateDate']
                # showTags = data['showTags']
                # gangweiyaoqiu = ''
                # gongzi = ''
                # fulitag = ''
                
                # for showTag in showTags:
                #     tag_type = showTag['type']
                #     if tag_type == 1:
                #         gongzi = showTag['name']
                #     if tag_type == 2:
                #         gangweiyaoqiu = gangweiyaoqiu + showTag['name'] + '|'
                #     if tag_type == 4:
                #         fulitag = fulitag + showTag['name'] + '|'

                jobId = data['id']
                detail_url = "https://www.yupao.com/zhaogong/" + str(jobId) + ".html"
                gongsimingcheng = get_detail(detail_url)
                jutididian = data['address']
                zhiweimingcheng = data['title']
                qitabiaoqian = data['desc']
                fabushijian = data['time']
                showTags = data['tmpShowTags']
                gangweiyaoqiu = ''
                gongzi = ''
                fulitag = ''
                
                for showTag in showTags:
                    tag_type = showTag['type']
                    if tag_type == 1:
                        gongzi = showTag['name']
                    if tag_type == 2:
                        gangweiyaoqiu = gangweiyaoqiu + showTag['name'] + '|'
                    if tag_type == 4:
                        fulitag = fulitag + showTag['name'] + '|'
                gongzi=data['salary']
                # 写入一行数据['具体地点', '职位名称', '工资', '福利tag', '公司名称', '公司标签', '其他标签', '岗位要求', '是否为推广', '会员商家', '发布时间', '抓取时间']
                writer.writerow({
                    '具体地点': jutididian,
                    '职位名称': zhiweimingcheng,
                    '工资': gongzi,
                    '福利tag': fulitag,
                    '公司名称': gongsimingcheng,
                    '公司标签': '',  # 这里假设没有公司标签
                    '其他标签': qitabiaoqian,
                    '岗位要求': gangweiyaoqiu,
                    '是否为推广': '',  # 这里假设没有推广信息
                    '会员商家': '',  # 这里假设没有会员商家信息
                    '发布时间': fabushijian,
                    '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            for row in existing_data:
                writer.writerow(row)

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except ValueError as e:
        print(f"解析响应 JSON 数据时发生错误: {e}")
    print("一次爬取完成，1小时后开始下次爬取")
    time.sleep(3600)