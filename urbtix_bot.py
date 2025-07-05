import json
import os
import time
import random
import re
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

def get_url_from_style(style_str):
    """
    從 style 屬性中提取圖片 URL
    """
    match = re.search(r'url\("(.*?)"\)', style_str)
    if match:
        return match.group(1)
    return None

def get_slide_distance(bg_url, slider_url, element_width):
    """
    使用 OpenCV 輪廓形狀比對計算滑塊需要移動的距離 (最終版：自適應閾值)
    """
    # 下載背景圖和滑塊圖
    bg_response = requests.get(bg_url)
    slider_response = requests.get(slider_url)

    # 儲存圖片到本機
    with open("background.png", "wb") as f:
        f.write(bg_response.content)
    with open("slider.png", "wb") as f:
        f.write(slider_response.content)
    print("[UrbTix] 已將背景圖和滑塊圖儲存到本機。")

    # 將圖片數據轉換為 OpenCV 格式
    bg_image = cv2.imdecode(np.frombuffer(bg_response.content, np.uint8), cv2.IMREAD_COLOR)
    slider_image = cv2.imdecode(np.frombuffer(slider_response.content, np.uint8), cv2.IMREAD_UNCHANGED)

    # --- 最終演算法：自適應閾值 + 形狀比對 + 品質檢查 ---
    original_bg_height, original_bg_width, _ = bg_image.shape
    print(f"[UrbTix] 圖片原始尺寸: 寬={original_bg_width}, 高={original_bg_height}")
    print(f"[UrbTix] 網頁元素尺寸: 寬={element_width}")

    # 1. 提取滑塊的輪廓 (目標形狀)
    if slider_image.shape[2] != 4:
        print("[UrbTix] 錯誤：滑塊圖片沒有 Alpha 通道。")
        return 0
    
    slider_alpha = slider_image[:, :, 3]
    _, slider_thresh = cv2.threshold(slider_alpha, 0, 255, cv2.THRESH_BINARY)
    slider_contours, _ = cv2.findContours(slider_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not slider_contours:
        print("[UrbTix] 錯誤：無法在滑塊圖片中找到輪廓。")
        return 0

    target_contour = max(slider_contours, key=cv2.contourArea)

    # 2. 使用自適應閾值處理背景圖，產生乾淨的二值化圖像
    bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    bg_thresh = cv2.adaptiveThreshold(bg_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    cv2.imwrite("background_threshold.png", bg_thresh) # 儲存二值化圖以供除錯
    print("[UrbTix] 已將背景二值化圖儲存為 background_threshold.png")

    # 在乾淨的二值化圖像上尋找輪廓
    bg_contours, _ = cv2.findContours(bg_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 3. 進行形狀比對，找出最相似的輪廓
    min_similarity = float('inf')
    best_match_contour = None

    for contour in bg_contours:
        similarity = cv2.matchShapes(target_contour, contour, cv2.CONTOURS_MATCH_I1, 0.0)
        if similarity < min_similarity:
            min_similarity = similarity
            best_match_contour = contour

    # 4. 計算座標、進行品質檢查並換算
    if best_match_contour is not None and min_similarity < 0.1: # 嚴格的品質檢查
        x, y, w, h = cv2.boundingRect(best_match_contour)
        print(f"[UrbTix] 在原始圖片中找到最相似輪廓: X={x}, 相似度={min_similarity:.4f}")
        
        # 計算縮放比例
        scale = element_width / original_bg_width
        print(f"[UrbTix] 座標縮放比例: {scale:.4f}")

        # 換算到網頁座標
        scaled_x = x * scale
        return scaled_x
    else:
        print(f"[UrbTix] 未能找到足夠相似的目標缺口 (最低相似度: {min_similarity:.4f})。")
        return 0

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
        time.sleep(5) # 等待 iframe 和圖片完全加載

        # 切換到驗證碼的 iframe
        print("[UrbTix] 正在等待 iframe 'tcaptcha_iframe_dy'...")
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'tcaptcha_iframe_dy')))
        print("[UrbTix] 已成功切換到 iframe。")

        # 獲取背景圖和滑塊圖的 URL
        print("[UrbTix] 正在定位背景圖...")
        bg_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#slideBg')))
        print("[UrbTix] 已成功定位背景圖。")
        # 獲取背景圖的 naturalWidth
        bg_natural_width = driver.execute_script("return arguments[0].naturalWidth;", bg_img_element)
        print(f"[UrbTix] 背景圖的 naturalWidth: {bg_natural_width}")
        print("[UrbTix] 正在定位滑塊圖...")
        slider_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='img_index=0']")))
        print("[UrbTix] 已成功定位滑塊圖。")
        
        # 測量網頁上背景圖的實際顯示寬度
        element_width = bg_img_element.size['width']

        bg_style = bg_img_element.get_attribute('style')
        slider_style = slider_img_element.get_attribute('style')

        bg_url = get_url_from_style(bg_style)
        slider_url = get_url_from_style(slider_style)

        print(f"[UrbTix] 背景圖 URL: {bg_url}")
        print(f"[UrbTix] 滑塊圖 URL: {slider_url}")
        print("[UrbTix] 已獲取驗證碼圖片 URL。")

        # 計算滑動距離
        distance = get_slide_distance(bg_url, slider_url, element_width)
        print(f"[UrbTix] 換算出的原始滑動距離為: {distance:.2f}px")

        # Round the final distance to an integer to avoid cumulative float errors
        distance = round(distance)
        print(f"[UrbTix] 四捨五入後的最終滑動距離: {distance}px")

        # 定位滑塊控制柄
        print("[UrbTix] 正在定位滑塊控制柄 'div.tc-slider-normal'...")
        slider_handle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.tc-slider-normal')))
        print("[UrbTix] 已成功定位滑塊控制柄。")

        # 執行人性化拖曳
        action = ActionChains(driver)
        action.click_and_hold(slider_handle)

        # 根據距離決定步數
        if distance < 50:
            num_steps = random.randint(2, 4)
        else:
            num_steps = random.randint(5, 10)

        # 生成隨機步長
        horizontal_steps = []
        remaining_distance = distance
        for i in range(num_steps - 1):
            max_step = remaining_distance - (num_steps - 1 - i) * 1 # 確保至少 1px 給剩餘步數
            if max_step <= 0:
                horizontal_steps.append(remaining_distance)
                remaining_distance = 0
                break
            step = random.uniform(1, max_step)
            horizontal_steps.append(step)
            remaining_distance -= step
        horizontal_steps.append(remaining_distance) # 將剩餘距離作為最後一步

        for dx in horizontal_steps:
            dy = random.randint(-3, 3) # 輕微的垂直偏移
            action.move_by_offset(dx, dy)
            action.pause(random.uniform(0.05, 0.15)) # 隨機的短暫停頓

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