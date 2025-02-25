from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import pdb
import time
import json

import crawl_51job
import crawl_yupao
import crawl_ganji
import crawl_58
import crawl_boss
import crawl_dianzhang

# print("开始抓取51job")
# crawl_51job.scrape_jobs_51job('jobs.csv')
# print("开始抓取yupao")
# crawl_yupao.scrape_jobs_yupao()
# print("开始抓取ganji")
# crawl_ganji.scrape_jobs_ganji('jobs.csv')
# print("开始抓取58")
# crawl_58.scrape_jobs_58('jobs.csv')
# print("开始抓取boss")
# crawl_boss.scrape_jobs_boss('jobs.csv')
print("开始抓取dianzhang")
crawl_dianzhang.scrape_jobs_dianzhang('jobs.csv')

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