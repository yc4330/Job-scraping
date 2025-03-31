import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime, timedelta
import pdb
import os
import json
import re
from DrissionPage import ChromiumPage, ChromiumOptions

def get_wlt(uids):
    # 定义URL和请求头
    userids = "|".join(uids)
    url = 'https://zpservice.58.com/api?returnType=1&action=wltStats,vipIdentity,brand,bzjStats,MpIndex&callback=jQuery110206068124689144796_1738890634817&params={"userIds":"'+userids+'"}&_=1738890634818'
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=tj%7C%E5%A4%A9%E6%B4%A5%7C0; id58=ChBPm2ej/MgKTlJyMyLSAg==; xxzlclientid=145ee298-1d0d-4aa0-9ce6-1738800329313; xxzlxxid=pfmxoe3D5g0rv57sApFy4AiwjCDiFdpnAyolVAbpq20FsvaDYO5PxEqUZI3xtuHv3lr/; wmda_uuid=cef99c8c775bd9616737d98bb4f2f8fd; wmda_new_uuid=1; city=bj; 58home=bj; isShowProtectTel=true; wmda_visited_projects=%3B1731916484865%3B10104579731767%3B1731918550401%3B2286118353409; 58tj_uuid=21b91442-3efc-4464-9852-2f982d51f73f; new_uv=1; als=0; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1739458604; sessionid=4687f491-fa0f-4cca-879b-b0940b1cb579; fzq_h=eec50c07bc1d0935958f91b5d0187e15_1741011982260_c5fa9ac0c9fd4bac8373730503fa9534_2099640508; www58com="UserID=59842467667220&UserName=glckyxci6"; 58cooper="userid=59842467667220&username=glckyxci6"; 58uname=glckyxci6; passportAccount="atype=0&bstate=0"; PPU=UID=59842467667220&UN=glckyxci6&TT=37fa52871f199974ee912613690504f7&PBODY=dBbaq57Dluh8_gLEScF8KC-IU8gD0B9M7RwvKl7yVRbVNHBoiGR-k_hKbFXCvh_8bis8J7E2gwU_YBivHxNdd10vmmeNLQ2JCjKCVKgJoGCo4UOZ9d2rDzjLotSJC-5lnlWIjcnlh5pAEtKo44yduxoO2f4d8JQw7pRBG82L2hY&VER=1&CUID=Ma45NaOktv8dHtzeROL7Dg; wmda_session_id_1731916484865=1741012023647-87a5df60-a943-472b-9478-7e0a14563bcd; f=n; wmda_report_times=2; fzq_js_zhaopin_list_pc=3c1647ab1ec4988b11f6e953b15e8d25_1741012041217_6; xxzlbbid=pfmbM3wxMDI5MnwxLjEwLjF8MTc0MTAxMjA0MjUwMDQ1NTI3OHxaUmZIQ0ZlYkRRbFYvVFVMcjByQXVXMTVPdjBOeE44bEtXVnh0dTNNTkxzPXxjZGRhNjgzNjIxNTg0NjgzZDc1NzM2MGU1ZmFkNzgwOV8xNzQxMDEyMDQyMzg4Xzc3NDhkNDAwZDRmOTQ5NWJiNDAyZjg4ZDJmZDJhMWE1XzIwOTk2NDA1MDh8MjY0NDQyOGU0MTE3NDExYWY4NWIyMTNlZGE4YjQ1NDRfMTc0MTAxMjA0MjExNV8yNTY=',
        'referer': 'https://bj.58.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)
    # 提取 JSON 部分
    json_str = re.search(r'\{.*\}', response.text).group()
    # 解析 JSON 数据
    data = json.loads(json_str)
    return data["wltStats"]["data"]


def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=tj%7C%E5%A4%A9%E6%B4%A5%7C0; id58=ChBPm2ej/MgKTlJyMyLSAg==; xxzlclientid=145ee298-1d0d-4aa0-9ce6-1738800329313; xxzlxxid=pfmxoe3D5g0rv57sApFy4AiwjCDiFdpnAyolVAbpq20FsvaDYO5PxEqUZI3xtuHv3lr/; wmda_uuid=cef99c8c775bd9616737d98bb4f2f8fd; wmda_new_uuid=1; city=bj; 58home=bj; isShowProtectTel=true; wmda_visited_projects=%3B1731916484865%3B10104579731767%3B1731918550401%3B2286118353409; 58tj_uuid=21b91442-3efc-4464-9852-2f982d51f73f; new_uv=1; als=0; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1739458604; sessionid=4687f491-fa0f-4cca-879b-b0940b1cb579; fzq_h=eec50c07bc1d0935958f91b5d0187e15_1741011982260_c5fa9ac0c9fd4bac8373730503fa9534_2099640508; www58com="UserID=59842467667220&UserName=glckyxci6"; 58cooper="userid=59842467667220&username=glckyxci6"; 58uname=glckyxci6; passportAccount="atype=0&bstate=0"; PPU=UID=59842467667220&UN=glckyxci6&TT=37fa52871f199974ee912613690504f7&PBODY=dBbaq57Dluh8_gLEScF8KC-IU8gD0B9M7RwvKl7yVRbVNHBoiGR-k_hKbFXCvh_8bis8J7E2gwU_YBivHxNdd10vmmeNLQ2JCjKCVKgJoGCo4UOZ9d2rDzjLotSJC-5lnlWIjcnlh5pAEtKo44yduxoO2f4d8JQw7pRBG82L2hY&VER=1&CUID=Ma45NaOktv8dHtzeROL7Dg; wmda_session_id_1731916484865=1741012023647-87a5df60-a943-472b-9478-7e0a14563bcd; f=n; wmda_report_times=2; fzq_js_zhaopin_list_pc=3c1647ab1ec4988b11f6e953b15e8d25_1741012041217_6; xxzlbbid=pfmbM3wxMDI5MnwxLjEwLjF8MTc0MTAxMjA0MjUwMDQ1NTI3OHxaUmZIQ0ZlYkRRbFYvVFVMcjByQXVXMTVPdjBOeE44bEtXVnh0dTNNTkxzPXxjZGRhNjgzNjIxNTg0NjgzZDc1NzM2MGU1ZmFkNzgwOV8xNzQxMDEyMDQyMzg4Xzc3NDhkNDAwZDRmOTQ5NWJiNDAyZjg4ZDJmZDJhMWE1XzIwOTk2NDA1MDh8MjY0NDQyOGU0MTE3NDExYWY4NWIyMTNlZGE4YjQ1NDRfMTc0MTAxMjA0MjExNV8yNTY='
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

def parse_page(html_content):
    co = ChromiumOptions()
    page = ChromiumPage(co)
    if html_content is None:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    job_items = soup.find_all('li', class_='job_item clearfix')
    data = []
    # 获取当前时间并格式化为 年-月-日 时:分:秒
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uids=[]
    print("抓取到数据:"+str(len(job_items))+"条")
    if len(job_items)==0:
        return []
    for item in job_items:
        uid=item.find('input').get('uid')
        uids.append(uid)
        location = item.find('span', class_='address')
        location = location.get_text(strip=True) if location else ''

        job_title = item.find('span', class_='name')
        job_title = job_title.get_text(strip=True) if job_title else ''
        
        salary = item.find('p', class_='job_salary')
        salary = salary.get_text(strip=True) if salary else ''
        
        welfare = item.find('div', class_='job_wel clearfix')
        if welfare is not None:
            welfares = welfare.findAll('span')
            welfare = ''
            for welfare_html in welfares:
                welfare += welfare_html.get_text(strip=True) if welfare_html else ''
                welfare += ' | '
        else:
            welfare=''
            
        company_name = item.find('a', class_='fl')
        company_name = company_name.get('title')
        # company_name = company_name.get_text(strip=True) if company_name else ''
        
        company_tag = item.find('div', class_='comp_name').find('i', class_='comp_icons')
        if company_tag is None:
            company_tag=''
        else:
            company_tag = company_tag.get('class')
            if len(company_tag)>1:
                company_tag=company_tag[1]
                if company_tag=="wlt":
                    company_tag=item.find('div', class_='comp_name').find('i', class_='comp_icons').get_text(strip=True)
                if company_tag=="mingqi":
                    company_tag="名企"
            else:
                company_tag=''
        
        other_tags = item.find('span', class_='tui_jian_txt')
        other_tags = other_tags.get_text(strip=True) if other_tags else ''
        
        job_requirements = item.find('p', class_='job_require')
        job_requirements = job_requirements.get_text(strip=True) if job_requirements else ''
        
        is_promoted = item.find('span', class_='sign')
        is_promoted = is_promoted.get_text(strip=True) if is_promoted else ''
        time_str=is_promoted
        formatted_time=''
        current_time_create = datetime.now()
        # 根据不同的时间描述修改当前时间
        if "分前" in time_str:
            minutes = int(time_str.replace("分前", ""))
            modified_time = current_time_create - timedelta(minutes=minutes)
            formatted_time = modified_time.strftime("%Y/%m/%d %H:%M:%S")
            is_promoted=''
        elif "小时前" in time_str:
            hours = int(time_str.replace("小时前", ""))
            modified_time = current_time_create - timedelta(hours=hours)
            formatted_time = modified_time.strftime("%Y/%m/%d %H:%M:%S")
            is_promoted=''
        elif "天前" in time_str:
            days = int(time_str.replace("天前", ""))
            modified_time = current_time_create - timedelta(days=days)
            formatted_time = modified_time.strftime("%Y/%m/%d %H:%M:%S")
            is_promoted=''
        else:
            modified_time = ''
        huiyuan_shangjia=""

        detail_url=item.find('div', class_='job_name clearfix').find('a').get('href')
        page.get(detail_url)
        page.wait.load_start()

        liulanrenshu=''
        shenqingrenshu=''
        zhaopinrenshu=''
        gongsirenshu=''
        xuelixianzhi=''
        jingyanxianzhi=''
        gongzuodizhi=''
        zhiweimiaoshu=''
        gongsijieshao=''
        gongsihangye=''
        renzhengleibie=''
        gongsizhaopinzhiweizongshu=''
        gongsileibie=''

        if page.eles('css:span[class="pos_base_num pos_base_browser"]'):
            liulanrenshu=page.eles('css:span[class="pos_base_num pos_base_browser"]')[0].text
        if page.eles('css:span[class="pos_base_num pos_base_apply"]'):
            shenqingrenshu=page.eles('css:span[class="pos_base_num pos_base_apply"]')[0].text
        if page.eles('css:span[class="item_condition pad_left_none"]'):
            zhaopinrenshu=page.eles('css:span[class="item_condition pad_left_none"]')[0].text
        if len(page.eles('css:span[class="item_condition"]'))>1:
            xuelixianzhi=page.eles('css:span[class="item_condition"]')[1].text
        if page.eles('css:span[class="item_condition border_right_None"]'):
            jingyanxianzhi=page.eles('css:span[class="item_condition border_right_None"]')[0].text
        if len(page.eles('css:div[class="pos-area"]')[0].children())>1:
            gongzuodizhi=page.eles('css:div[class="pos-area"]')[0].children()[1].text
        if page.eles('css:div[class="des"]'):
            zhiweimiaoshu=page.eles('css:div[class="des"]')[0].text
        if page.eles('css:div[class="shiji"]'):
            gongsijieshao=page.eles('css:div[class="shiji"]')[0].text
        if page.eles('css:a[class="comp_baseInfo_link"]'):
            gongsihangye=page.eles('css:a[class="comp_baseInfo_link"]')[0].text
        if page.eles('css:p[class="comp_baseInfo_scale"]'):
            gongsirenshu=page.eles('css:p[class="comp_baseInfo_scale"]')[0].text
        if page.eles('css:div[class="identify_title"]'):
            renzhengleibie=page.eles('css:div[class="identify_title"]')[0].text
        if page.eles('css:a[class="baseInfo_link"]'):
            zhaopinrenshu=page.eles('css:a[class="baseInfo_link"]')[0].text
        # page.close()
        # 将数据添加到列表中，按照指定顺序
        data.append([
            location,
            job_title,
            salary,
            welfare,
            company_name,
            company_tag,
            other_tags,
            job_requirements,
            is_promoted,
            huiyuan_shangjia,
            formatted_time,
            current_time,
            '58',
            liulanrenshu,
            shenqingrenshu,
            zhaopinrenshu,
            gongsirenshu,
            xuelixianzhi,
            jingyanxianzhi,
            gongzuodizhi,
            zhiweimiaoshu,
            gongsijieshao,
            gongsihangye,
            renzhengleibie,
            gongsizhaopinzhiweizongshu,
            gongsileibie
        ])
        # 定义字段顺序
        columns = [
            '具体地点',
            '职位名称',
            '工资',
            '福利tag',
            '公司名称',
            '公司标签',
            '其他标签',
            '岗位要求',
            '是否为推广',
            '会员商家',
            '发布时间',
            '抓取时间',
            '平台',
            '浏览人数',
            '申请人数',
            '招聘人数',
            '公司人数',
            '学历限制',
            '经验限制',
            '工作地址',
            '职位描述',
            '公司介绍',
            '公司行业',
            '认证类别',
            '公司招聘职位总数',
            '公司类别',
        ]

    wtls=get_wlt(uids)
    for wlt_i in range(len(data)):
        data[wlt_i][9]=wtls[uids[wlt_i]]
        if len(data[wlt_i][9].split("wlt"))>1:
            wlt_year=data[wlt_i][9].split("wlt")[1]
            data[wlt_i][9]="58同城会员商家"+str(wlt_year)+"年"
        if data[wlt_i][9]=="_empty":
            data[wlt_i][9]=""
    return data

def save_to_csv(data, filename='jobs_58.csv'):
    headers = [
        '具体地点',
        '职位名称',
        '工资',
        '福利tag',
        '公司名称',
        '公司标签',
        '其他标签',
        '岗位要求',
        '是否为推广',
        '会员商家',
        '发布时间',
        '抓取时间',
        '平台',
        '浏览人数',
        '申请人数',
        '招聘人数',
        '公司人数',
        '学历限制',
        '经验限制',
        '工作地址',
        '职位描述',
        '公司介绍',
        '公司行业',
        '认证类别',
        '公司招聘职位总数',
        '公司类别',
    ]
    # headers = ['具体地点', '职位名称', '工资', '福利tag', '公司名称', '公司标签', '其他标签', '岗位要求', '是否为推广', '会员商家', '发布时间', '抓取时间', '平台']
    # data.insert(0,headers)
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)
    deduplicated_data = []
    unique_job_titles = set()
    if file_exists:
        existing_data = []
        with open(filename, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            existing_data = list(reader)
        existing_data=existing_data[1:]
        data.extend(existing_data)
    for data_one in data:
        job_title=data_one[1]
        if job_title not in unique_job_titles:
            unique_job_titles.add(job_title)
            deduplicated_data.append(data_one)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(deduplicated_data)

def read_file(file_path='爬取到多少页_58.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件中的内容
            return file.read().strip()
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
        return 0  # 如果文件不存在，返回0
    except ValueError:
        print(f"文件 {file_path} 的内容无效。")
        return 0  # 如果文件内容不是数字，返回0

def scrape_jobs_58(filename='jobs_58.csv'):
    page_count=read_file()
    page_count=int(page_count.split("页")[0])
    search_key=read_file('搜索关键词.txt')
    for url_index in range(1,page_count+1):
        print("当前爬取到"+str(url_index)+"页")
        if url_index==1:
            url = 'https://bj.58.com/pugongjg/?key='+str(search_key)+'&classpolicy=strategy%2Cuuid_4b48dfe2ca954a1aa7a36aad27d906a3%2Cdisplocalid_1%2Cfrom_413249%2Cto_jump%2Ctradeline_job%2Cclassify_C&search_uuid=4b48dfe2ca954a1aa7a36aad27d906a3&final=1'
        else:
            url = 'https://bj.58.com/pugongjg/pn'+str(url_index)+'/?key='+str(search_key)+'&classpolicy=strategy%2Cuuid_4b48dfe2ca954a1aa7a36aad27d906a3%2Cdisplocalid_1%2Cfrom_413249%2Cto_jump%2Ctradeline_job%2Cclassify_C&search_uuid=4b48dfe2ca954a1aa7a36aad27d906a3&final=1'
        html_content = get_page_content(url)
        parsed_data = parse_page(html_content)
        save_to_csv(parsed_data,filename)
    print("抓取完成，数据保存到jobs.csv")

if __name__ == '__main__':
    scrape_jobs_58()