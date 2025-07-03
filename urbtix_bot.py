import json
import os
import time
import random
import requests
import cv2
import numpy as np
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def load_settings():
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_slide_distance(bg_url, slider_url):
    """
    使用 OpenCV 計算滑塊需要移動的距離
    """
    # 下載背景圖和滑塊圖
    bg_response = requests.get(bg_url)
    slider_response = requests.get(slider_url)

    # 將圖片數據轉換為 OpenCV 格式
    bg_image = cv2.imdecode(np.frombuffer(bg_response.content, np.uint8), cv2.IMREAD_COLOR)
    slider_image = cv2.imdecode(np.frombuffer(slider_response.content, np.uint8), cv2.IMREAD_COLOR)

    # 轉換為灰階
    bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    slider_gray = cv2.cvtColor(slider_image, cv2.COLOR_BGR2GRAY)

    # 邊緣檢測
    bg_edges = cv2.Canny(bg_gray, 100, 200)
    slider_edges = cv2.Canny(slider_gray, 100, 200)

    # 模板匹配
    result = cv2.matchTemplate(bg_edges, slider_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 返回最佳匹配位置的 x 座標
    return max_loc[0]

def run():
    settings = load_settings()["urbtix"]
    print("[UrbTix] 讀取設定檔...")
    print(f"[UrbTix] 帳號: {settings['username']}")
    print(f"[UrbTix] 登入網址: {settings['event_url']}")

    print("[UrbTix] 啟動瀏覽器...")
    driver = uc.Chrome()
    driver.get(settings['event_url'])
    wait = WebDriverWait(driver, 20)
    time.sleep(2)

    # 自動填寫帳號密碼
    try:
        # 等待並填寫帳號
        login_id_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="loginId"]')))
        login_id_input.click()
        login_id_input.send_keys(settings['username'])

        # 等待並填寫密碼
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.click()
        password_input.send_keys(settings['password'])
        print("[UrbTix] 已自動填寫帳號密碼")

        # 點擊登入按鈕
        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.login-button')))
        driver.execute_script("arguments[0].click();", login_btn)
        print("[UrbTix] 已自動點擊登入按鈕，等待驗證碼...")

    except Exception as e:
        print(f"[UrbTix] 自動填寫登入資訊失敗: {e}")
        driver.quit()
        return

    # --- 電腦視覺滑塊驗證 ---
    try:
        print("[UrbTix] 偵測到滑塊驗證碼，啟動電腦視覺分析...")
        time.sleep(3) # 等待 iframe 和圖片完全加載

        # 切換到驗證碼的 iframe
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'tcaptcha_iframe_dy')))
        print("[UrbTix] 已成功切換到 iframe。")

        # 獲取背景圖和滑塊圖的 URL
        bg_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.yidun_bg-img')))
        slider_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.yidun_jigsaw')))
        
        bg_url = bg_img_element.get_attribute('src')
        slider_url = slider_img_element.get_attribute('src')
        print("[UrbTix] 已獲取驗證碼圖片 URL。")

        # 計算滑動距離
        distance = get_slide_distance(bg_url, slider_url)
        # 實際拖曳距離需要微調，減去滑塊左邊的空白部分
        distance -= 6 
        print(f"[UrbTix] OpenCV 計算出的滑動距離為: {distance}px")

        # 定位滑塊控制柄
        slider_handle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.tc-slider-normal')))
        
        # 執行人性化拖曳
        action = ActionChains(driver)
        action.click_and_hold(slider_handle)
        
        # 分段移動
        action.move_by_offset(distance * 0.7, random.randint(-5, 5)).pause(random.uniform(0.2, 0.4))
        action.move_by_offset(distance * 0.3, random.randint(-3, 3)).pause(random.uniform(0.1, 0.3))
        action.release().perform()

        print("[UrbTix] 已根據計算結果嘗試自動滑動驗證碼。")
        driver.switch_to.default_content()
        time.sleep(5)

    except Exception as e:
        print(f"[UrbTix] 自動滑動驗證碼失敗: {e}")
        driver.switch_to.default_content()
        print("[UrbTix] 請手動完成驗證，完成後按 Enter 繼續...")
        input()

    # ...後續流程...
    print("[UrbTix] 登入成功或驗證完成，請檢查頁面。")
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    run()