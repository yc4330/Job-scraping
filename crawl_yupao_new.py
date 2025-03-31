from DrissionPage import ChromiumPage
import pandas as pd
from datetime import datetime
import traceback
import os
import time

def scrape_jobs_yupao():
    with open('搜索关键词.txt', 'r', encoding='utf-8') as file:
        search_key = file.read().strip()

    page = ChromiumPage()
    page.get(f'https://www.yupao.com/topic/a2c0/?keywords={search_key}')
    page.wait.load_start()

    data = []  # 确保数据不会被清空

    while True:
        try:
            while len(page.eles('css:main')) == 0:
                pass

            data_indexs = page.eles('css:main')[0].child().children()
            print(f"抓取到 {len(data_indexs)} 条数据")

            for data_index in data_indexs:
                try:
                    if data_index.attr('class'):
                        continue

                    job_name = data_index.eles('css:h3')[0].text  
                    salary = data_index.eles('css:span')[0].text  
                    publish_time = data_index.eles('css:span')[1].text  
                    other_tags = data_index.eles('css:p')[0].text  
                    location = data_index.eles('css:p')[1].text  

                    data_index.click()
                    new_tab = page.latest_tab
                    new_tab.wait.load_start()

                    if new_tab.ele('xpath://*[text()="点击进行验证"]'):
                        while new_tab.ele('xpath://*[text()="点击进行验证"]'):
                            time.sleep(0.5)

                    gangweiyaoqiu = '|'.join([a.text for a in new_tab.eles('css:main')[0].ele('css:div').ele('css:div').children()[1].eles('css:a')])
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

                except Exception as e:
                    print(f"数据解析失败: {e}")
                    traceback.print_exc()

            # 确保数据不会丢失
            if data:
                df = pd.DataFrame(data)
                df.to_csv('jobs.csv', mode='a', index=False, encoding='utf-8-sig', header=not os.path.exists('jobs.csv'))
                print("数据已追加到 jobs.csv")
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

if __name__ == '__main__':
    scrape_jobs_yupao()
