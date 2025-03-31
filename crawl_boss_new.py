from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time

storage_state_file = "account.json"

def scrape_jobs_boss(filename='jobs_boss.csv'):
    file = open('搜索关键词.txt', 'r', encoding='utf-8')
    # 读取文件内容
    search_key_boss = file.read()
    # 关闭文件
    file.close()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",args=["--mute-audio"])
        # browser = p.chromium.launch(headless=False, executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--mute-audio"])
        # 尝试加载已保存的登录状态
        if os.path.exists(storage_state_file):
            context = browser.new_context(storage_state=storage_state_file)
            print("加载已保存的登录信息...")
            page = context.new_page()
            page.goto("https://www.zhipin.com/web/geek/job?query="+str(search_key_boss)+"&city=101010100&page=1")
            time.sleep(3)
            while True:
                # 等待页面加载完成
                # page.wait_for_selector('.job-name')

                # 获取所有职位信息
                while True:
                    pass
                    jobs = page.query_selector_all('.job-card-wrapper')
                    if len(jobs)>0:
                        break

                job_data = []

                for job in jobs:
                    # 提取各个字段
                    job_name = job.query_selector('.job-name')
                    job_area = job.query_selector('.job-area')
                    salary = job.query_selector('.salary')
                    company_name = job.query_selector('.company-name')
                    info_desc = job.query_selector('.info-desc')
                    job_info = job.query_selector('.job-info.clearfix')
                    job_card_footer = job.query_selector('.job-card-footer')
                    company_tag_list = job.query_selector('.company-tag-list')

                    # 提取文本内容
                    job_name_text = job_name.inner_text() if job_name else ''
                    job_area_text = job_area.inner_text() if job_area else ''
                    salary_text = salary.inner_text() if salary else ''
                    company_name_text = company_name.inner_text() if company_name else ''
                    info_desc_text = info_desc.inner_text() if info_desc else ''
                    info_desc_text=''
                    job_info_text = '|'.join([li.inner_text() for li in job_info.query_selector_all('.tag-list li')]) if job_info else ''
                    job_card_footer_text = job_card_footer.inner_text() if job_card_footer else ''
                    company_tag_list_text = '|'.join([li.inner_text() for li in company_tag_list.query_selector_all('li')]) if company_tag_list else ''

                    new_page = context.new_page()
                    new_page.goto("https://www.zhipin.com"+job.query_selector_all('a[class="job-card-left"]')[0].get_attribute('href'))
                    # 其他字段
                    other_tags = ''
                    is_promoted = ''
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
                        xuelixianzhi=new_page.query_selector_all('span[class="text-desc text-degree"]')[0].text_content()
                        jingyanxianzhi=new_page.query_selector_all('span[class="text-desc text-experiece"]')[0].text_content()
                        # aaa=new_page.query_selector_all('span[class="boss-active-time"]')[0].text_content()#近半年活跃
                        if new_page.query_selector_all('div[class="job-sec-text fold-text"]'):
                            gongsijieshao=new_page.query_selector_all('div[class="job-sec-text fold-text"]')[0].text_content()
                        if new_page.query_selector_all('li[class="company-type"]'):
                            gongsileixing=new_page.query_selector_all('li[class="company-type"]')[0].text_content()
                        gongzuodizhi=new_page.query_selector_all('div[class="location-address"]')[0].text_content()
                        gongsirenshu=new_page.query_selector_all('i[class="icon-scale"]')[0].text_content()
                        gongsihangye=new_page.query_selector_all('a[ka="job-detail-brandindustry"]')[0].text_content()
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
                        'boss',
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

                print("boss抓取到数据"+str(len(job_data))+"条")
                # 将数据保存到CSV文件
                df = pd.DataFrame(job_data, columns=columns)

                # 检查文件是否存在
                if os.path.exists(filename):
                    existing_df = pd.read_csv(filename, encoding='utf-8-sig')

                    # 从第二行开始插入新数据
                    result_df = pd.concat([df, existing_df[0:]], ignore_index=True)

                    # 将更新后的数据重新写入 CSV 文件
                    result_df.to_csv(filename, index=False, encoding='utf-8-sig')
                else:
                    # 如果文件不存在，则创建新文件并写入表头
                    df.to_csv(filename, index=False, encoding='utf-8-sig')
                next_page_button=page.query_selector_all('.options-pages')[0].query_selector_all('a')[-1]
                if next_page_button.get_attribute('class')=="disabled":
                    break
                else:
                    next_page_button.click()
        # 关闭浏览器
        browser.close()
if __name__ == '__main__':
    scrape_jobs_boss()