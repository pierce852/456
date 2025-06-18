# 專案安裝指南

本專案需要安裝以下兩個工具以運行自動化瀏覽器測試：**ChromeDriver** 和 **Selenium**。請按照以下步驟完成安裝。

## 1. 安裝 ChromeDriver

**ChromeDriver** 是一個用於驅動 Chrome 瀏覽器的工具，需與您當前使用的 Chrome 瀏覽器版本一致。

### 安裝步驟：
1. **檢查 Chrome 版本**：
   - 打開 Chrome 瀏覽器，點擊右上角的「三點」菜單，選擇「說明」 > 「關於 Google Chrome」。
   - 記下當前 Chrome 的版本號（例如：130.0.6723.69）。
2. **下載 ChromeDriver**：
   - 訪問 [ChromeDriver 下載頁面](https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-tw)。
   - 選擇與您 Chrome 版本匹配的 ChromeDriver 版本進行下載。
3. **安裝 ChromeDriver**：
   - **Windows**：
     - 將下載的 `chromedriver.exe` 解壓縮並移動到一個固定路徑（例如：`C:\chromedriver`）。
     - 將該路徑添加到系統環境變數的 `Path` 中。
   - **MacOS/Linux**：
     - 將下載的 `chromedriver` 解壓縮並移動到 `/usr/local/bin` 或其他系統路徑：
       ```bash
       sudo mv chromedriver /usr/local/bin/
       sudo chmod +x /usr/local/bin/chromedriver

## 2. 安裝 Selenium

Selenium 是一個用於自動化網頁操作的 Python 庫，可通過 pip 安裝。

安裝步驟：
打開終端機（Terminal）或命令提示字元（Command Prompt）。
輸入以下指令以安裝 Selenium：
 pip install selenium