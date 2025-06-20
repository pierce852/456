import json
import os
import undetected_chromedriver as uc
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
    settings = load_settings()["urbtix"]
    print("[UrbTix] 讀取設定檔...")
    print(f"[UrbTix] 帳號: {settings['username']}")
    print(f"[UrbTix] 登入網址: {settings['event_url']}")
    print(f"[UrbTix] 票種: {settings['ticket_type']}")
    print(f"[UrbTix] 數量: {settings['ticket_quantity']}")

    print("[UrbTix] 啟動瀏覽器...")
    driver = uc.Chrome()
    driver.get(settings['event_url'])
    wait = WebDriverWait(driver, 15)
    time.sleep(2)

    # 自動填寫帳號密碼
    try:
        login_id_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="loginId"]')))
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="請輸入密碼"]')
        login_id_input.send_keys(settings['username'])
        password_input.send_keys(settings['password'])
        print("[UrbTix] 已自動填寫帳號密碼")
        # 點擊登入按鈕
        login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_btn.click()
        print("[UrbTix] 已自動點擊登入按鈕，等待驗證碼...")
    except Exception as e:
        print(f"[UrbTix] 自動填寫登入資訊失敗: {e}")

    # 半自動化：偵測驗證碼提示
    time.sleep(2)
    page_source = driver.page_source
    if ("驗證碼" in page_source) or ("验证码" in page_source) or ("滑块" in page_source) or ("滑塊" in page_source):
        print("[UrbTix] 偵測到驗證碼，請手動完成驗證，完成後按 Enter 繼續...")
        input()

    # ...後續流程可繼續自動搶票...
    time.sleep(5)
    driver.quit()

    print("[UrbTix] 登入帳號...")
    print("[UrbTix] 進入搶票頁面...")
    print("[UrbTix] 自動刷新與搶票...")
    print("[UrbTix] 選擇票種/區域/數量...")
    print("[UrbTix] 處理驗證碼（如需手動則提示）...")
    print("[UrbTix] 提交訂單...")
    print("[UrbTix] 完成，請檢查結果或留意音效提醒。") 