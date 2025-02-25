from playwright.sync_api import sync_playwright
import time
import pdb
import json

storage_state_file = "yupao_account.json"
# 保存 cookies 和 localStorage 到文件
def save_login_state(context, filename=storage_state_file):
    cookies = context.cookies()
    local_storage = context.storage_state()  # 保存 localStorage 等信息
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"cookies": cookies, "local_storage": local_storage}, f)

def login():
    with sync_playwright() as p:
        # 启动浏览器（设置 headless=False 可以观察浏览器行为）
        browser = p.chromium.launch(headless=False,executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",args=["--mute-audio"])
        context = browser.new_context()
        
        page = context.new_page()
        page.goto("https://www.yupao.com/")
        pdb.set_trace()
        
        save_login_state(context)
        # 关闭浏览器
        browser.close()

if __name__ == "__main__":
    login()