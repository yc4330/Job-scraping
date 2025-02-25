from DrissionPage import ChromiumPage
import pandas as pd
from datetime import datetime
import traceback
import pdb

def scrape_jobs_yupao():
    # 读取搜索关键词
    with open('搜索关键词.txt', 'r', encoding='utf-8') as file:
        search_key = file.read().strip()

    # 初始化浏览器页面
    page = ChromiumPage()
    page.get(f'https://www.yupao.com/topic/a2c0/?keywords={search_key}')
    page.wait.load_start()
    while True:
        pass
        # 初始化一个空列表来存储数据
        data = []

        try:
            # 获取所有具备 data-index 属性的 div 标签
            while len(page.eles('css:main'))==0:
                pass
            data_indexs = page.eles('css:main')[0].child().children()
            print("抓取到"+str(len(data_indexs))+"条数据")
            for data_index in data_indexs:
                # 跳过有 class 属性的元素
                if data_index.attr('class'):
                    continue

                # 提取职位信息
                job_name = data_index.eles('css:h3')[0].text  # 职位名称
                salary = data_index.eles('css:span')[0].text  # 工资
                publish_time = data_index.eles('css:span')[1].text  # 发布时间
                other_tags = data_index.eles('css:p')[0].text  # 其它标签
                location = data_index.eles('css:p')[1].text  # 具体地点
                # detail_url = data_index.eles('css:a')[0].attr('href')  # 详情页链接

                # 打开新标签页并访问详情页
                data_index.click()
                new_tab = page.latest_tab
                # new_tab = page.new_tab()
                # new_tab.get(detail_url)
                new_tab.wait.load_start()
                gangweiyaoqiu=''
                gangweiyaoqius=new_tab.eles('css:main')[0].ele('css:div').ele('css:div').children()[1].eles('css:a')
                for gangweiyaoqiu_a in gangweiyaoqius:
                    gangweiyaoqiu += gangweiyaoqiu_a.text + '|'
                # 提取福利标签
                fuli_tag = ''
                fuli_tags = new_tab.eles('css:main')[0].ele('css:div').ele('css:div').children()[2].eles('css:span')
                for fuli_tag_index in range(1, len(fuli_tags)):
                    fuli_tag += fuli_tags[fuli_tag_index].text + '|'
                company_name=new_tab.eles('xpath://*[text()="公司名称："]')
                if len(company_name)==0:
                    company_name=''
                else:
                    company_name=company_name[0].parent().children()[1].text
                # 关闭详情页标签页
                new_tab.close()
                # 将数据添加到列表
                data.append({
                    '具体地点': location,
                    '职位名称': job_name,
                    '工资': salary,
                    '福利tag': fuli_tag,
                    '公司名称': company_name,  # 如果需要提取公司名称，可以在这里添加逻辑
                    '公司标签': '',  # 如果需要提取公司标签，可以在这里添加逻辑
                    '其他标签': other_tags,
                    '岗位要求': gangweiyaoqiu,  # 如果需要提取岗位要求，可以在这里添加逻辑
                    '是否为推广': '',  # 如果需要提取是否为推广，可以在这里添加逻辑
                    '会员商家': '',  # 如果需要提取会员商家，可以在这里添加逻辑
                    '发布时间': publish_time,
                    '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    '平台': '鱼泡'
                })

        except Exception as e:
            tb = traceback.format_exc()
            print(f"发生错误: {e}\n错误堆栈信息:\n{tb}")
            pdb.set_trace()

        # 将数据保存到 CSV 文件
        if data:
            df = pd.DataFrame(data)
            try:
                # 如果 CSV 文件已存在，追加数据
                existing_df = pd.read_csv('jobs.csv')
                df = pd.concat([existing_df, df], ignore_index=True)
            except FileNotFoundError:
                # 如果 CSV 文件不存在，创建新文件
                pass
            df.to_csv('jobs.csv', index=False, encoding='utf-8-sig')
            print("数据已保存到 jobs.csv")
        else:
            print("未抓取到数据")
        if page.eles('css:main')[0].child().children()[-3].children()[-2].style("background-color")=='rgb(0, 146, 255)':
            break
        page.eles('css:main')[0].child().children()[-3].children()[-1].click()


if __name__ == '__main__':
    scrape_jobs_yupao()