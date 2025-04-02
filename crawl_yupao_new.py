from DrissionPage import ChromiumPage
import pandas as pd
from datetime import datetime
import traceback
import os
import time


def scrape_jobs_yupao(target_num):
    with open('搜索关键词.txt', 'r', encoding='utf-8') as file:
        search_key = file.read().strip()

    page = ChromiumPage()
    page.get(f'https://www.yupao.com/topic/a2c0/?keywords={search_key}')
    page.wait.load_start()

    data = []  # 确保数据不会被清空

    scraped_num = 0     # track data scraped

    past_data = pd.read_csv("merged_jobs_deduplicate_new.csv") # dir of all past data to deduplicate
    past_data = past_data[past_data['平台'] == "鱼泡"]

    # while True:
    # for i in range(2):
    while scraped_num < target_num:
        try:
            while len(page.eles('css:main')) == 0:
                pass

            data_indexes = page.eles('css:main')[0].child().children()
            # print(f"抓取到 {len(data_indexes)} 条数据")

            for data_index in data_indexes:
                try:
                    if data_index.attr('class'):
                        continue

                    job_name = data_index.eles('css:h3')[0].text  
                    salary = data_index.eles('css:span')[0].text  
                    publish_time = data_index.eles('css:span')[1].text  
                    other_tags = data_index.eles('css:p')[0].text  
                    location = data_index.eles('css:p')[1].text  
                    
                    # 验证是否重复
                    # 通过job_name
                    if len(past_data[past_data['职位名称'] == job_name]) >0:
                        print(f"duplicated {job_name}, skipped...")
                        continue

                    # 点击详情页
                    data_index.click()
                    new_tab = page.latest_tab
                    new_tab.wait.load_start()

                    if new_tab.ele('xpath://*[text()="点击进行验证"]'):
                        while new_tab.ele('xpath://*[text()="点击进行验证"]'):
                            time.sleep(0.5)
                    
                    time.sleep(0.5)
                    gangweiyaoqiu = '|'.join([a.text for a in new_tab.eles('css:main')[0].ele('css:div').ele('css:div').children()[1].eles('css:a')])
                    ###### 有时会出现out of index 的情况？######

                    fuli_tag = '|'.join([s.text for s in new_tab.eles('css:main')[0].ele('css:div').ele('css:div').children()[2].eles('css:span')[1:]])

                    company_name = new_tab.eles('xpath://*[text()="公司名称："]')
                    company_name = company_name[0].parent().children()[1].text if company_name else ''

                    if new_tab != page:
                        new_tab.close()

                    data.append({
                        '具体地点': location,
                        '职位名称': job_name,
                        '工资': salary,
                        '福利tag': fuli_tag,
                        '公司名称': company_name,
                        '其他标签': other_tags,
                        '岗位要求': gangweiyaoqiu,
                        '发布时间': publish_time,
                        '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        '平台': '鱼泡'
                    })
                    scraped_num+=1      # track scraped number
                    if scraped_num >= target_num:
                        break

                except Exception as e:
                    print(f"数据解析失败: {e}")
                    traceback.print_exc()

            # 确保数据不会丢失
            if data:
                df = pd.DataFrame(data)
                # 用日期命名
                today_date = datetime.now().strftime("%m%d")
                csv_filename=f"new_data/jobs_yupao_{today_date}.csv"

                df.to_csv(csv_filename, mode='a', index=False, encoding='utf-8-sig', header=not os.path.exists(csv_filename))
                print(f"{len(data)}行数据已追加到 {csv_filename}")
                data.clear()  # 追加后清空数据列表，防止重复写入

            if page.eles('css:main')[0].child().children()[-3].children()[-2].style("background-color") == 'rgb(0, 146, 255)':
                break

            page.eles('css:main')[0].child().children()[-3].children()[-1].click()

        except Exception as e:
            print(f"发生错误: {e}")
            traceback.print_exc()
            try:
                if page.ele('xpath://*[text()="点击进行验证"]'):
                    while page.ele('xpath://*[text()="点击进行验证"]'):
                        time.sleep(1)
                page.eles('css:main')[0].child().children()[-3].children()[-1].click()
            except Exception:
                pass
    print(f"鱼泡 共抓取到数据{scraped_num}条")


if __name__ == '__main__':
    scrape_jobs_yupao(200)      # input: how many data entires to collect
