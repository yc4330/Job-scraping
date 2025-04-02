from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

storage_state_file = "account.json"

def scrape_jobs_51job(target_num):

    # 用日期命名保存的文件 e.g. "jobs_51_0331.csv"
    today_date = datetime.now().strftime("%m%d")
    csv_filename=f"new_data/jobs_51_{today_date}.csv"

    file = open('搜索关键词.txt', 'r', encoding='utf-8')
    # 读取文件内容
    search_key_boss = file.read()
    # 关闭文件
    file.close()

    page_index = 1      # track page number
    scraped_num = 0     # track data scraped

    # 微去重
    past_data = pd.read_csv("merged_jobs_deduplicate_new.csv") # dir of all past data to deduplicate
    past_data = past_data[past_data['平台'] == "51"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",args=["--mute-audio"])
        # browser = p.chromium.launch(headless=True, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--headless=new","--mute-audio"])
        # browser = p.chromium.launch(headless=False, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--mute-audio"])
        # 尝试加载已保存的登录状态
        if os.path.exists(storage_state_file):
            context = browser.new_context(storage_state=storage_state_file)
            print("加载已保存的登录信息...")
            page = context.new_page()
            page.goto("https://we.51job.com/pc/search?jobArea=010000&keyword="+str(search_key_boss)+"")
            
            # for page_index in range(1,2):
            while scraped_num < target_num:
                nolist = page.query_selector_all('div[class="j_nolist"]')
                if len(nolist)>0:
                    break
                # 等待页面加载完成
                # page.wait_for_selector('.joblist')

                # 获取所有职位信息
                while True:
                    pass
                    joblists = page.query_selector_all('.joblist')  # 替换为实际的职位卡片选择器
                    if len(joblists)>0:
                        break
                while True:
                    pass
                    jobs = joblists[0].query_selector_all('div[sensorsname="JobShortExposure"]')
                    if len(jobs)>0:
                        break
                job_data = []

                for job_biaoqian in jobs:
                    try:
                        job = json.loads(job_biaoqian.get_attribute("sensorsdata"))
                        jobId = job["jobId"]
                        job_name_text = job["jobTitle"]
                        job_area_text = job["jobArea"]
                        salary_text = job["jobSalary"]
                        company_name_text = job_biaoqian.query_selector('a[class="cname text-cut"]').get_attribute("title")
                        info_desc_text=''
                        job_info_text=''
                        job_card_footer_text=''
                        if job_biaoqian.query_selector('div[class="tags"]'):
                            job_card_footer_text_divs = job_biaoqian.query_selector('div[class="tags"]').query_selector_all('div')
                        else:
                            job_card_footer_text_divs=''
                        for job_card_footer_text_div in job_card_footer_text_divs:
                            job_card_footer_text=job_card_footer_text+job_card_footer_text_div.inner_text()+'|'
                        company_tag_list_text=''
                        company_tag_list_text_divs=job_biaoqian.query_selector_all('span[class="dc text-cut"]')+job_biaoqian.query_selector_all('span[class="dc shrink-0"]')
                        for company_tag_list_text_div in company_tag_list_text_divs:
                            company_tag_list_text += company_tag_list_text_div.inner_text()+'|'
                        # 其他字段
                        other_tags = ''
                        is_promoted = ''
                        is_vip = ''
                        publish_time = ''
                        scrape_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        liulanrenshu=''
                        if len(job_biaoqian.query_selector_all('span[class="tip shrink-0"]'))>0:
                            liulanrenshu=job_biaoqian.query_selector_all('span[class="tip shrink-0"]')[-1].text_content()
                        zhaopinrenshu=job_biaoqian.query_selector_all('span[class="dc shrink-0"]')[-1].text_content()
                        xuelixianzhi=job["jobDegree"]
                        jingyanxianzhi=job["jobYear"]
                        gongzuodizhi=job_area_text
                        if len(job_biaoqian.query_selector_all('span[class="dc text-cut"]'))>0:
                            gongsihangye=job_biaoqian.query_selector_all('span[class="dc text-cut"]')[-1].text_content()
                        # new_page.close()

                        # 验证是否重复
                        # 通过以上信息
                        if len(past_data[(past_data['职位名称'] == job_name_text) &
                                     (past_data['具体地点'] == job_area_text) & 
                                     (past_data['工资'] == salary_text) &
                                     (past_data['公司名称'] == company_name_text) &
                                     (past_data['其他标签'] == info_desc_text) &
                                     (past_data['岗位要求'] == job_info_text) &
                                     (past_data['公司标签'] == company_tag_list_text)]) >0:
                            print(f"duplicated {job_name_text}, skipped...")
                            continue

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
                            '51job',
                            liulanrenshu,
                            '',
                            zhaopinrenshu,
                            '',
                            xuelixianzhi,
                            jingyanxianzhi,
                            gongzuodizhi,
                            '',
                            '',
                            gongsihangye,
                            '',
                            '',
                            ''
                        ])

                        scraped_num+=1      # track scraped number
                        if scraped_num >= target_num:
                            break

                    except Exception as e:
                        pass

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

                print("51job抓取到数据"+str(len(job_data))+"条")
                
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
                    page.query_selector_all('li.number')[4].click()
                else:
                    page.query_selector_all('li.number')[page_index].click()
                
                page_index+=1   # next page

        print(f"51job 共抓取到数据{scraped_num}条")
        # 关闭浏览器
        browser.close()

if __name__ == '__main__':
    scrape_jobs_51job(2000)