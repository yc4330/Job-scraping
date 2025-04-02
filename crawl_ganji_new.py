from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

storage_state_file = "account.json"

def scrape_jobs_ganji(target_num):

    # 用日期命名
    today_date = datetime.now().strftime("%m%d")
    csv_filename=f"new_data/jobs_ganji_{today_date}.csv"

    file = open('搜索关键词.txt', 'r', encoding='utf-8')
    # 读取文件内容
    search_key_boss = file.read()
    # 关闭文件
    file.close()

    scraped_num = 0     # track data scraped

    # 微去重
    past_data = pd.read_csv("merged_jobs_deduplicate_new.csv") # dir of all past data to deduplicate
    past_data = past_data[past_data['平台'] == "赶集"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",args=["--mute-audio"])
        # browser = p.chromium.launch(headless=False, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--mute-audio"])
        # browser = p.chromium.launch(headless=True, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--headless=new","--mute-audio"])
        # 尝试加载已保存的登录状态
        if os.path.exists(storage_state_file):
            context = browser.new_context(storage_state=storage_state_file)
            print("加载已保存的登录信息...")
            page = context.new_page()
            page.goto("https://bj.ganji.com/job/pn1/?key="+str(search_key_boss)+"")

            # for page_index in range(1,2):
            page_index = 1  # track page index to change page
            while scraped_num < target_num:     # track scraped number
                # 等待页面加载完成
                # page.wait_for_selector('.position-card')

                # 获取所有职位信息
                while True:
                    pass
                    jobs = page.query_selector_all('.position-card')
                    if len(jobs)>0:
                        break
                time.sleep(10)
                jobs = jobs[0].query_selector_all('div[class="dataCollectionCls"]')
                job_data = []

                for job_biaoqian in jobs:
                    job_info_text=''
                    # 提取文本内容
                    job_name_text = job_biaoqian.query_selector('li[class="ibox-title"]').inner_text()

                    # 验证是否重复
                    # 通过job_name
                    if len(past_data[past_data['职位名称'] == job_name_text]) >0:
                        print(f"duplicated {job_name_text}, skipped...")
                        continue

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
                    company_tag_list_text=''

                    # 其他字段
                    other_tags = ''
                    is_vip = ''
                    publish_time = ''
                    scrape_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

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
                    try:
                        jingyanxianzhi=new_page.query_selector_all('p[class="detail-position-require"]')[0].text_content().split(' · ')[0]
                        xuelixianzhi=new_page.query_selector_all('p[class="detail-position-require"]')[0].text_content().split(' · ')[1]
                        zhaopinrenshu=new_page.query_selector_all('p[class="detail-position-require"]')[0].text_content().split(' · ')[2]
                        gongzuodizhi=new_page.query_selector_all('p[class="detail-position-address"]')[0].text_content()
                        zhiweimiaoshu=new_page.query_selector_all('p[class="detail-desc-position"]')[0].text_content()
                        gongsijieshao=new_page.query_selector_all('p[class="detail-desc-company"]')[0].text_content()
                        gongsihangye=new_page.query_selector_all('p[class="detail-company-content-type"]')[0].text_content()
                        gongsirenshu=new_page.query_selector_all('p[class="detail-company-content-type"]')[1].text_content()
                        renzhengleibie=new_page.query_selector_all('p[class="detail-company-content-type-auth"]')[0].text_content()
                    except Exception as e:
                        pass
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
                        '赶集',
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

                    scraped_num+=1      # track number scraped
                    if scraped_num >= target_num:
                        break

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

                print("赶集抓取到数据"+str(len(job_data))+"条")

                # scraped_num += len(job_data)    # track scraped number

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

                page_index+=1      # track page index to change page

        print("赶集 共抓取到数据"+scraped_num+"条")
        # 关闭浏览器
        browser.close()

if __name__ == '__main__':
    scrape_jobs_ganji(1000)       # input: how many data entires to collect