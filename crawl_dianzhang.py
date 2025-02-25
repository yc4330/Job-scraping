from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

storage_state_file = "account.json"

def scrape_jobs_dianzhang(filename="jobs_店长.csv"):
    file = open('搜索关键词.txt', 'r', encoding='utf-8')
    # 读取文件内容
    search_key_boss = file.read()
    # 关闭文件
    file.close()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",args=["--mute-audio"])
        # browser = p.chromium.launch(headless=True, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--headless=new","--mute-audio"])
        # 尝试加载已保存的登录状态
        if os.path.exists(storage_state_file):
            context = browser.new_context(storage_state=storage_state_file)
            print("加载已保存的登录信息...")
            page = context.new_page()
            for page_index in range(1,11):
                page.goto("https://www.dianzhangzhipin.com/joblist/?cityCode=7&query="+str(search_key_boss)+"&page="+str(page_index))
                # 等待页面加载完成
                page.wait_for_selector('.job-list')

                # 获取所有职位信息
                jobs = page.query_selector_all('.job-list')  # 替换为实际的职位卡片选择器
                jobs = jobs[0].query_selector_all('li')
                job_data = []

                for job_biaoqian in jobs:
                    # 提取文本内容
                    job_name_text = job_biaoqian.query_selector('div[class="job-title"]').inner_text()
                    salary_text = job_biaoqian.query_selector('span[class="red"]').inner_text()
                    company_name_text = job_biaoqian.query_selector('a[class="info-company"]').inner_text()
                    info_desc_text=''
                    job_card_footer_text=''
                    is_promoted = ''
                    company_tag_list_text=''

                    # 其他字段
                    other_tags = ''
                    is_vip = ''
                    publish_time = ''
                    scrape_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

                    job_info_text=''
                    detail_url="https://www.dianzhangzhipin.com"+job_biaoqian.query_selector("a").get_attribute("href")
                    new_page = context.new_page()
                    new_page.goto(detail_url)
                    new_page.wait_for_selector('p[class="other"]')#job-tags
                    job_info_str = new_page.query_selector('p[class="other"]').inner_html()
                    job_area_text=job_info_str.split('<em class="dolt"> </em>')[0]
                    job_info_text="|".join(job_info_str.split('<em class="dolt"> </em>')[1].split('<em class="dolt"></em>')[:-1])
                    job_card_footer_spans=new_page.query_selector('div[class="job-tags"]').query_selector_all('span')
                    for job_card_footer_span in job_card_footer_spans:
                        job_card_footer_text+=job_card_footer_span.inner_text()+'|'
                    new_page.close()

                    # 将数据添加到列表中，按照指定顺序
                    job_data.append([
                        job_area_text,  # 具体地点
                        job_name_text,  # 职位名称
                        salary_text,  # 工资
                        job_card_footer_text,  # 福利tag
                        company_name_text,  # 公司名称
                        company_tag_list_text,  # 公司标签
                        info_desc_text,  # 其他标签
                        job_info_text,  # 岗位要求
                        is_promoted,  # 是否为推广
                        is_vip,  # 会员商家
                        publish_time,  # 发布时间
                        scrape_time,
                        '店长'
                    ])

                # 定义字段顺序
                columns = [
                    '具体地点', '职位名称', '工资', '福利tag', '公司名称', '公司标签', '其他标签', '岗位要求', '是否为推广', '会员商家', '发布时间', '抓取时间', '平台'
                ]
                print("店长抓取到数据"+str(len(job_data))+"条")
                csv_filename=filename
                # 将数据保存到CSV文件
                df = pd.DataFrame(job_data, columns=columns)

                # 检查文件是否存在
                if os.path.exists(csv_filename):
                    existing_df = pd.read_csv(csv_filename, encoding='utf-8-sig')

                    # 从第二行开始插入新数据
                    result_df = pd.concat([df, existing_df[0:]], ignore_index=True)

                    # 将更新后的数据重新写入 CSV 文件
                    result_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
                else:
                    # 如果文件不存在，则创建新文件并写入表头
                    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        # 关闭浏览器
        browser.close()