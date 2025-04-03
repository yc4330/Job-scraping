# %%
import pandas as pd
import re
from datetime import datetime
import subprocess
import os

# %%
current_directory = os.getcwd()
today_date = datetime.now().strftime("%m%d")

# Define file paths
all_jobs = os.path.join(current_directory, "cleaned_jobs.csv")
new_file = os.path.join(current_directory, f"new_jobs_{today_date}.csv")

# Check if the local file exists
if os.path.exists(all_jobs):
    # Read both files
    local_df = pd.read_csv(all_jobs)
    new_df = pd.read_csv(new_file)

    # 找出 new_df 中不在 local_df 的那部分
    subset_cols = ['具体地点', '职位名称', '工资', '福利tag', '公司名称']
    merged = new_df.merge(local_df[subset_cols], on=subset_cols, how='left', indicator=True)
    merged_df = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
else:
    # If the local file does not exist, use the new file as the base
    merged_df = pd.read_csv(new_file)

# %%
column_list = ['平台', '发布时间', '抓取时间', 'Scraped_date', '具体地点', '工作地址', 'District', '工资',
       'Pay_time', 'Wage_average', 'Wage_min', 'Wage_max', '职位名称', '福利tag',
       '其他标签', '职位描述', 'Category', '岗位要求', '学历限制', '经验限制', 'education',
       'experience', '公司名称', '公司标签',
       '是否为推广', '会员商家', '浏览人数', '申请人数', '招聘人数', '公司人数','company_size', '公司介绍', '公司行业', '认证类别',
       '公司招聘职位总数', '公司类别', 'bonus.perform', 'bonus.dividend',
       'bonus.commission', 'bonus.year', 'bonus.quarter', 'bonus.month',
       'bonus.week', 'bonus.other', 'holiday.overtime-pay', 'holiday.pay',
       'holiday.legal', 'leave.medical', 'leave.wedding', 'leave.pregnancy',
       'leave.hazard', 'leave.ocuppied', 'leave.funeral',
       'social.insurance.commercial', 'social.insurance.only.medical',
       'social.insurance.only.pension', 'social.insurance.only.unemploy',
       'social.insurance.only.workinjury', 'social.insurance.only.maternity',
       'social.insurance.five', 'social.insurance.sixth',
       'social.insurance.unspecified', 'social.fund.housing',
       'accommodation.aid', 'accommodation.included', 'accommodation.dorm',
       'meal.aid', 'meal.included', 'meal.cafe', 'transport.aid',
       'transport.shuttle', 'transport.included', 'training',
       'medical.physical', 'promotion', 'worklife.flexible', 'worklife.snack',
       'worklife.less-overtime', 'worklife.altdaysoff', 'compensation.heat',
       'compensation.cold', 'compensation.overtime', 'compensation.night',
       'compensation.comm', 'compensation.free-uniform', 'Accomodation','Meal','Insurance','Compensation','Bonus','Holiday']

# %%
for col in column_list:
    if col not in merged_df.columns:
        merged_df[col] = None

merged_df = merged_df[column_list]

# %%
print(merged_df.columns)

# %%
merged_df['Scraped_date'] = pd.to_datetime(merged_df['抓取时间'], errors='coerce').dt.date

# %%
# Define the district dictionary
district_dic = ["朝阳", "通州", "丰台", "东城", "西城", "大兴", "房山", "昌平", "顺义", "海淀", "密云", "怀柔", "平谷","门头沟", "石景山", "延庆","北京"]

# Function to find district
def find_district(row):
    for district in district_dic:
        if district in str(row['具体地点']) or district in str(row['工作地址']):
            return district
    return None

merged_df['District'] = merged_df.apply(find_district, axis=1)
merged_df = merged_df[merged_df['District'].notnull()]

# %%
def clean_wage(text):
    if not isinstance(text, str):
        return text
    if '时' in text:
        return '时结'
    if '天' in text:
        return '日结'
    if '月' in text or 'K' in text or '千' in text or '万' in text:
        return '月结'
    if '面议' in text:
        return '面议'
    if '单' in text:
        return '按单结'
    return text
merged_df['Pay_time'] = merged_df['工资'].apply(clean_wage)

# %%
def parse_salary(salary):
    """Extracts min and max wage from salary strings and converts to numbers."""
    if not isinstance(salary, str):
        return None, None

    # Remove unwanted characters (like "·13薪" or spaces)
    salary = re.sub(r'[^\d\.万千\-]', '', salary)

    # Convert Chinese numerical suffixes properly
    salary = re.sub(r'(\d+\.?\d*)万', lambda x: str(float(x.group(1)) * 10000), salary)
    salary = re.sub(r'(\d+\.?\d*)千', lambda x: str(float(x.group(1)) * 1000), salary)

    # Extract numbers
    numbers = re.findall(r'\d+\.?\d*', salary)

    # Convert numbers to float
    numbers = [float(num) for num in numbers]

    # Ensure values less than 50 are scaled correctly (likely meant to be thousands)
    numbers = [num * 1000 if num < 50 else num for num in numbers]

    # Return appropriate min and max values
    if len(numbers) == 1:
        return int(numbers[0]), int(numbers[0])  # If only one number, set both min and max to the same value
    elif len(numbers) == 2:
        return int(numbers[0]), int(numbers[1])
    return None, None


# %%
# Update Wage_min and Wage_max for rows where Pay_time is '月结'
salary_data = merged_df.loc[merged_df['Pay_time'] == '月结', "工资"].apply(parse_salary)
salary_min, salary_max = zip(*salary_data) if not salary_data.empty else ([], [])
merged_df.loc[merged_df['Pay_time'] == '月结', "Wage_min"] = salary_min
merged_df.loc[merged_df['Pay_time'] == '月结', "Wage_max"] = salary_max
merged_df['Wage_average'] = (merged_df['Wage_min'] + merged_df['Wage_max']) / 2

# %%
# 需要检查的列
check_columns = ['职位名称', '福利tag', '其他标签', '职位描述']

# 定义关键词字典
keywords_dict = {
    "bonus.perform": ["绩效"],
    "bonus.dividend": ["分红"],
    "bonus.commission": ["提成"],
    "bonus.year": ["年终奖"],
    "bonus.quarter": ["季度奖"],
    "bonus.month": ["月度奖"],
    "bonus.week": ["周奖"],
    "bonus.other": ["奖金", "奖励"],
    "holiday.overtime-pay": ["双薪", "三薪", "四薪", "五薪", "六薪", "七薪", "八薪", "九薪", "十薪"],
    "holiday.pay": ["带薪年假", "带薪休假", "年假"],
    "holiday.legal": ["法定假"],
    "leave.medical": ["病假"],
    "leave.wedding": ["婚假"],
    "leave.pregnancy": ["产假", "产检假"],
    "leave.hazard": ["工伤假"],
    "leave.ocuppied": ["事假"],
    "leave.funeral": ["丧假"],
    "social.insurance.commercial": ["商业保险"],
    "social.insurance.only.medical": ["医保", "医疗保险"],
    "social.insurance.only.pension": ["养老保险"],
    "social.insurance.only.unemploy": ["失业保险"],
    "social.insurance.only.workinjury": ["工伤保险"],
    "social.insurance.only.maternity": ["生育保险"],
    "social.insurance.five": ["五险", "六险"],
    "social.insurance.sixth": ["六险"],
    "social.insurance.unspecified": ["社保"],
    "social.fund.housing": ["五险一金", "公积金"],
    "accommodation.aid": ["房补", "分配住宿", "住宿补贴"],
    "accommodation.included": ["吃住", "包住", "提供住宿"],
    "accommodation.dorm": ["宿舍"],
    "meal.aid": ["餐补", "饭补"],
    "meal.included": ["包餐", "管饭", "包吃", "管吃", "三餐", "免费餐", "吃住", "包三餐", "包早餐", "包午餐", "包晚餐"],
    "meal.cafe": ["食堂"],
    "transport.aid": ["交通补助", "车费补贴", "车贴", "车补", "交通费", "公交卡", "地铁卡", "油卡", "停车费", "过路费", "高速费"],
    "transport.shuttle": ["班车", "接送"],
    "transport.included": ["报销路费", "报销车费", "车费报销"],
    "training": ["培训", "学习机会"],
    "medical.physical": ["体检"],
    "promotion": ["晋升", "升职", "晋级", "职业发展", "职业规划"],
    "worklife.flexible": ["弹性工作", "灵活工作"],
    "worklife.snack": ["零食下午茶"],
    "worklife.less-overtime": ["加班少"],
    "worklife.altdaysoff": ["调休"],
    "compensation.heat": ["高温补贴"],
    "compensation.cold": ["寒冷补贴"],
    "compensation.overtime": ["加班补贴"],
    "compensation.night": ["夜班补贴"],
    "compensation.comm": ["通讯补贴", "话补"],
    "compensation.free-uniform": ["免费工装"]
}

# 需要排除的关键词（适用于特定的 bonus.other 和保险筛选）
exclude_dict = {
    "bonus.other": ["年终奖", "季度奖", "月度奖", "周奖"],
    "social.insurance.only.medical": ["五险", "六险"],
    "social.insurance.only.pension": ["五险", "六险"],
    "social.insurance.only.unemploy": ["五险", "六险"],
    "social.insurance.only.workinjury": ["五险", "六险"],
    "social.insurance.only.maternity": ["五险", "六险"],
    "social.insurance.unspecified": ["五险", "六险", "医保", "医疗保险", "养老保险", "失业保险", "工伤保险", "生育保险"]
}

def check_keywords(text, keywords):
    if pd.isna(text):
        return False
    return any(keyword in text for keyword in keywords)

def check_exclude(text, exclude_list):
    if pd.isna(text):
        return False
    return any(keyword in text for keyword in exclude_list)

# 初始化新列
for col in keywords_dict.keys():
    merged_df[col] = 0

# 遍历数据框，检查每行文本
for index, row in merged_df.iterrows():
    combined_text = " ".join(str(row[col]) for col in check_columns if pd.notna(row[col]))
    
    for col, keywords in keywords_dict.items():
        if col in exclude_dict:
            if check_keywords(combined_text, keywords) and not check_exclude(combined_text, exclude_dict[col]):
                merged_df.at[index, col] = 1
        else:
            if check_keywords(combined_text, keywords):
                merged_df.at[index, col] = 1

# %%
merged_df['Accomodation'] = merged_df[['accommodation.aid', 'accommodation.included', 'accommodation.dorm']].max(axis=1)
merged_df['Meal'] = merged_df[['meal.aid', 'meal.included', 'meal.cafe']].max(axis=1)
merged_df['Insurance'] = merged_df[['social.insurance.commercial', 'social.insurance.only.medical', 'social.insurance.only.pension', 'social.insurance.only.unemploy', 'social.insurance.only.workinjury', 'social.insurance.only.maternity', 'social.insurance.five', 'social.insurance.sixth', 'social.insurance.unspecified','social.fund.housing']].max(axis=1)
merged_df['Compensation'] = merged_df[['compensation.heat', 'compensation.cold', 'compensation.overtime', 'compensation.night', 'compensation.comm', 'compensation.free-uniform']].max(axis=1)
merged_df['Bonus'] = merged_df[['bonus.perform', 'bonus.dividend', 'bonus.commission', 'bonus.year', 'bonus.quarter', 'bonus.month', 'bonus.week', 'bonus.other']].max(axis=1)
merged_df['Holiday'] = merged_df[['holiday.overtime-pay', 'holiday.pay', 'holiday.legal', 'leave.medical', 'leave.wedding', 'leave.pregnancy', 'leave.hazard', 'leave.ocuppied', 'leave.funeral']].max(axis=1)

# %%
def categorize_experience(experience):
    if pd.isna(experience):
        return None
    if "不限" in experience or "无需" in experience:
        return "不限"
    if "在校" in experience or "应届" in experience:
        return "在校/应届"
    return experience

# Apply the function to the '经验限制' column
merged_df['经验限制'] = merged_df['经验限制'].apply(categorize_experience)

# Remove "及以上", "以下" and "经验" from the '经验限制' column
merged_df['经验限制'] = merged_df['经验限制'].str.replace("及以上", "").replace("以内", "").str.replace("以下", "").str.replace("经验", "").str.strip()

# %%
# Define the function to categorize education levels
def categorize_education(level):
    if pd.isna(level):
        return None
    if any(x in level for x in ["高中", "中专", "中技", "职高", "技校"]):
        return "高中/中专/中技/职高/技校"
    if "初中" in level:
        return "初中"
    if "本科" in level:
        return "本科"
    if "硕士" in level:
        return "硕士"
    if "大专" in level:
        return "大专"
    return "不限"

# Apply the function to the '学历限制' column
merged_df['学历限制'] = merged_df['学历限制'].apply(categorize_education)

# %%
merged_df = merged_df.drop_duplicates(subset=['具体地点', '职位名称', '工资', '福利tag', '公司名称'])

# %%
education_mapping = {
    '不限': 0,
    '初中': 1,
    '高中/中专/中技/职高/技校': 2,
    '大专': 3,
    '本科': 4,
    '硕士': 5
}

merged_df['education'] = merged_df['学历限制'].map(education_mapping)


# %%
# Define the mapping function
def map_experience(exp):
    if exp in ['不限', '在校/应届']:
        return 0
    elif not pd.isna(exp):
        match = re.search(r"\d+", exp)
        return int(match.group()) if match else None

# Apply the mapping function to create the 'experience' column
merged_df['experience'] = merged_df['经验限制'].apply(map_experience)

# %%
# 提取公司人数并映射到对应类别的函数
def map_company_size(text):
    if isinstance(text, float) and pd.isna(text):
        return None  # 处理异常情况
    
    numbers = re.findall(r"\d+", str(text))  # 提取所有数字
    if not numbers:
        return None  # 处理异常情况
    
    min_size = int(numbers[0])  # 取第一个数字作为最小值

    # 映射规则
    if min_size < 10:
        return 1
    elif min_size < 50:
        return 2
    elif min_size < 100:
        return 3
    elif min_size < 500:
        return 4
    elif min_size < 1000:
        return 5
    else:
        return 6

# 应用于 DataFrame
merged_df["company_size"] = merged_df["公司人数"].apply(map_company_size)

# %%
# save the DataFrame to a new CSV file
merged_df.to_csv(f"cleaned_jobs_{today_date}.csv", index=False)


# %%
# Define file paths
all_jobs = os.path.join(current_directory, "cleaned_jobs.csv")
new_file = os.path.join(current_directory, f"cleaned_jobs_{today_date}.csv")

# Check if the local file exists
if os.path.exists(all_jobs):
    # Read both files
    local_df = pd.read_csv(all_jobs)
    new_df = pd.read_csv(new_file)
    
    # Merge the dataframes and drop duplicates
    df = pd.concat([local_df, new_df]).drop_duplicates(subset=['具体地点', '职位名称', '工资', '福利tag', '公司名称'])
else:
    # If the local file does not exist, use the new file as the base
    df = pd.read_csv(new_file)

# Save the merged dataframe back to the local file
df.to_csv(all_jobs, index=False)