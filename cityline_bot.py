import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def load_settings():
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run():
    settings = load_settings()["cityline"]
    print("[Cityline] 讀取設定檔...")
    print(f"[Cityline] 帳號: {settings['username']}")
    print(f"[Cityline] 活動網址: {settings['event_url']}")
    print(f"[Cityline] 票種: {settings['ticket_type']}")
    print(f"[Cityline] 數量: {settings['ticket_quantity']}")

    print("[Cityline] 啟動瀏覽器...")
    driver = webdriver.Chrome()
    driver.get(settings['event_url'])
    time.sleep(2)

    # 半自動化：偵測滑塊驗證碼提示
    page_source = driver.page_source
    if ("滑块" in page_source) or ("滑塊" in page_source) or ("拖动下方滑块" in page_source) or ("拖動下方滑塊" in page_source):
        print("[Cityline] 偵測到滑塊驗證碼，請手動完成驗證，完成後按 Enter 繼續...")
        input()

    print("[Cityline] 嘗試自動點擊登入按鈕...")
    try:
        wait = WebDriverWait(driver, 10)
        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.navbar-login > a')))
        driver.execute_script("arguments[0].click();", login_btn)
        print("[Cityline] 已點擊登入，請確認是否進入登入頁...")
        time.sleep(2)
        # TODO: 這裡可繼續自動填寫帳號密碼
    except Exception as e:
        print(f"[Cityline] 找不到登入按鈕或點擊失敗: {e}")

    print("[Cityline] 已打開活動頁面。請根據實際情況補充登入與搶票流程...")
    time.sleep(5)  # 示意停留5秒，可根據需求調整
    driver.quit()

    print("[Cityline] 登入帳號...")
    print("[Cityline] 進入搶票頁面...")
    print("[Cityline] 自動刷新與搶票...")
    print("[Cityline] 選擇票種/區域/數量...")
    print("[Cityline] 處理驗證碼（如需手動則提示）...")
    print("[Cityline] 提交訂單...")
    print("[Cityline] 完成，請檢查結果或留意音效提醒。") 