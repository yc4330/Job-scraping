from DrissionPage import ChromiumPage
import json
import pdb
import pandas as pd
import pdb
# 创建 ChromiumPage 对象
file = open('搜索关键词.txt', 'r', encoding='utf-8')
# 读取文件内容
search_key = file.read()
# 关闭文件
file.close()
page = ChromiumPage()
searchKey="公交"
# 打开目标页面
page.get('https://www.yupao.com/topic/a2c0/?keywords='+search_key)
page.wait.load_start()
pdb.set_trace()
# 初始化一个空列表来存储数据
data = []

try:
    items = page.eles('css:div[class^="index_search-item-center"]')
    for item in items:
        company_name = item.eles('css:a[class^="index_alink"]')[0].text  # 公司名称
        if not all(char in company_name for char in searchKey):
            continue
        registration_status = item.eles('css:span[class^="index_tag-status"]')[0].text  # 登记状态
        taxpayer_id = item.eles('css:div[class^="index_info-row"]')[0].eles('css:div[class^="index_info-col"]')[3].ele('css:span').text  # 纳税人识别号
        legal_representative = item.eles('css:div[class^="index_info-row"]')[0].eles('css:div[class^="index_info-col"]')[0].ele('css:span').text  # 法人
        registered_capital = item.eles('css:div[class^="index_info-row"]')[0].eles('css:div[class^="index_info-col"]')[1].ele('css:span').text  # 注册资本
        establishment_date = item.eles('css:div[class^="index_info-row"]')[0].eles('css:div[class^="index_info-col"]')[2].ele('css:span').text  # 成立日期
        registration_address = item.eles('css:span[class^="index_value"]')[4].text  # 注册地址

        # 分割注册地址
        province = ""
        city = ""
        district = ""
        try:
            temp_registration_address=registration_address
            # 简单的地址分割逻辑，可根据实际情况调整
            parts = temp_registration_address.split("省")
            if len(parts) >= 2:
                province = parts[0]+"省"
                temp_registration_address=parts[1]
            parts = temp_registration_address.split("市")
            if len(parts) >= 2:
                city = parts[0]+"市"
                temp_registration_address=parts[1]
            district=temp_registration_address
        except Exception as e:
            print(f"地址分割出错: {e}")

        detail_url = item.eles('css:a[class^="index_alink"]')[0].attr('href')
        # 打开一个新标签页
        new_tab = page.new_tab()
        # 在新标签页中访问指定的 URL
        new_tab.get(detail_url)

        # 等待新标签页加载完成
        new_tab.wait.load_start()
        legal_litigation = new_tab.eles('css:span[class^="index_nav-num"]')[1].text  # 法律诉讼
        business_risk = new_tab.eles('css:span[class^="index_nav-num"]')[2].text  # 经营风险
        # 关闭新标签页（如果需要）
        new_tab.close()

        # 将数据添加到列表中
        data.append({
            '注册地址_省': province,
            '注册地址_市': city,
            '注册地址_所属地区': district,
            '公司名称': company_name,
            '登记状态': registration_status,
            '纳税人识别号': taxpayer_id,
            '法人': legal_representative,
            '注册资本': registered_capital,
            '成立日期': establishment_date,
            '注册地址': registration_address,
            '法律诉讼': legal_litigation+"条",
            '经营风险': business_risk+"条",
            '详情链接': detail_url
        })

except Exception as e:
    print(f"出现错误: {e}")

# 将数据保存到 Excel 文件
try:
    # 尝试读取已有的 Excel 文件
    existing_df = pd.read_excel('company_info.xlsx')
    new_df = pd.DataFrame(data)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_excel('company_info.xlsx', index=False)
except FileNotFoundError:
    # 如果文件不存在，直接保存新数据
    df = pd.DataFrame(data)
    df.to_excel('company_info.xlsx', index=False)

# 关闭页面和浏览器
page.quit()