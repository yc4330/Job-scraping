from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

storage_state_file = "account.json"

def scrape_jobs_ganji(csv_filename="jobs_ganji.csv"):
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
            page.goto("https://bj.ganji.com/job/pn3/?key="+str(search_key_boss)+"")
            for page_index in range(2,30):
                # 等待页面加载完成
                # page.wait_for_selector('.position-card')

                # 获取所有职位信息
                while True:
                    pass
                    jobs = page.query_selector_all('.position-card')
                    if len(jobs)>0:
                        break
                jobs = jobs[0].query_selector_all('div[class="dataCollectionCls"]')
                job_data = []

                for job_biaoqian in jobs:
                    job_info_text=''
                    detail_url=job_biaoqian.query_selector("a").get_attribute("href")
                    new_page = context.new_page()
                    new_page.goto(detail_url)
                    while True:
                        pass
                        try:
                            new_page.wait_for_selector('p[class="detail-position-require"]')
                            job_info_text = new_page.query_selector('p[class="detail-position-require"]').inner_text()
                            break
                        except Exception as e:
                            pass
                    new_page.close()
                    # 提取文本内容
                    job_name_text = job_biaoqian.query_selector('li[class="ibox-title"]').inner_text()
                    job_area_text = job_biaoqian.query_selector('li[class="ibox-address"]').inner_text().split("｜")[0]
                    salary_text = job_biaoqian.query_selector('li[class="ibox-salary"]').inner_text()
                    company_name_text = job_biaoqian.query_selector('li[class="ibox-enterprise"]').inner_text()
                    info_desc_text=''
                    job_card_footer_text=''
                    is_promoted = ''
                    if job_biaoqian.query_selector_all('span.ibox-icon-item'):
                        job_card_footer_text_divs = job_biaoqian.query_selector_all('span.ibox-icon-item')
                    else:
                        job_card_footer_text_divs=''
                    for job_card_footer_text_div in job_card_footer_text_divs:
                        if job_card_footer_text_div.inner_text()=="广告" and job_card_footer_text_div.get_attribute("style")!="display:none;":
                            is_promoted='推广广告'
                        else:
                            if job_card_footer_text_div.inner_text()!="广告" and job_card_footer_text_div.get_attribute("style")!="display:none;":
                                job_card_footer_text=job_card_footer_text+job_card_footer_text_div.inner_text()+'|'
                    company_tag_list_text=''

                    # 其他字段
                    other_tags = ''
                    is_vip = ''
                    publish_time = ''
                    scrape_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

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
                        '赶集'
                    ])
                print("赶集抓取到数据"+str(len(job_data))+"条")

                # 定义字段顺序
                columns = [
                    '具体地点', '职位名称', '工资', '福利tag', '公司名称', '公司标签', '其他标签', '岗位要求', '是否为推广', '会员商家', '发布时间', '抓取时间', '平台'
                ]
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
                if page_index>4:
                    page.query_selector_all('a.button')[4].click()
                else:
                    page.query_selector_all('a.button')[page_index].click()
        # 关闭浏览器
        browser.close()