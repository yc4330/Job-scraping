from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

import crawl_51job_new
import crawl_yupao_new
import crawl_ganji_new
import crawl_58_new
import crawl_boss_new
import crawl_dianzhang_new

# print("开始抓取51job")
# crawl_51job_new.scrape_jobs_51job('51_jobs.csv')
# print("开始抓取yupao")
# crawl_yupao_new.scrape_jobs_yupao()
# print("开始抓取ganji")
# crawl_ganji_new.scrape_jobs_ganji('ganji_jobs_newnew.csv')
# print("开始抓取58")
# crawl_58_new.scrape_jobs_58('58_jobs_newnew.csv')
# print("开始抓取boss")
# crawl_boss_new.scrape_jobs_boss('boss_jobs_newnew.csv')
print("开始抓取dianzhang")
crawl_dianzhang_new.scrape_jobs_dianzhang('dianzhang_jobs_newnew.csv')

import csv

# 输入和输出 CSV 文件的路径
input_file = 'jobs.csv'
output_file = 'norepeat_jobs.csv'

# 用于存储已经出现过的第二列的值
seen_values = set()

# 存储处理后的数据
cleaned_rows = []

# 读取输入的 CSV 文件
with open(input_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) >= 2:
            second_column_value = row[1]
            if second_column_value not in seen_values:
                seen_values.add(second_column_value)
                cleaned_rows.append(row)

# 将处理后的数据写入输出的 CSV 文件
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(cleaned_rows)

print(f"处理完成，结果已保存到 {output_file}")