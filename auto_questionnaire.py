#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NKUST 問卷自動填寫系統
流程：登入 → 主頁 → 期末問卷 → 期末問卷填寫 → 各科填寫問卷 → 送出
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import config

class QuestionnaireAutoFiller:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_browser(self):
        """設定 Microsoft Edge 瀏覽器"""
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
        except:
            self.driver = webdriver.Edge(options=options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        """步驟1: 登入系統"""
        print("🔐 步驟1: 開始登入...")
        self.driver.get(config.LOGIN_URL)
        time.sleep(3)
        
        # 填入帳號密碼
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        username_input.send_keys(config.STUDENT_ID)
        password_input.send_keys(config.PASSWORD)
        print(f"✅ 已填入帳號: {config.STUDENT_ID}")
        
        # 等待 reCAPTCHA 驗證
        print("⚠️ 請完成 reCAPTCHA 驗證")
        print("✋ 完成後請點擊任意鍵繼續...")
        
        # 等待用戶確認
        try:
            import msvcrt
            print("📝 按任意鍵繼續...")
            msvcrt.getch()  # Windows 下等待按鍵
        except ImportError:
            # 非 Windows 系統使用 input
            input("📝 按 Enter 繼續...")
        
        # 點擊登入按鈕
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        time.sleep(5)
        print("✅ 登入成功")
        
    def navigate_to_questionnaire_list(self):
        """步驟2-4: 導航到問卷列表"""
        print("\n🏠 步驟2: 已進入主頁")
        time.sleep(3)  # 增加等待時間讓頁面完全載入
        
        # 調試：顯示當前頁面狀態
        print("🔍 檢查頁面內容...")
        try:
            page_title = self.driver.title
            current_url = self.driver.current_url
            print(f"📄 頁面標題: {page_title}")
            print(f"🌐 當前網址: {current_url}")
        except:
            pass
        
        print("📋 步驟3: 尋找期末問卷選單...")
        try:
            # 嘗試多種方式尋找期末問卷
            menu_selectors = [
                "//a[contains(text(),'期末問卷')]",
                "//span[contains(text(),'期末問卷')]", 
                "//div[contains(text(),'期末問卷')]",
                "//li[contains(text(),'期末問卷')]",
                "//*[contains(text(),'期末問卷')]"
            ]
            
            final_exam_menu = None
            for selector in menu_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        final_exam_menu = elements[0]
                        print(f"✅ 找到期末問卷選單: {selector}")
                        break
                except:
                    continue
            
            if final_exam_menu:
                # 滾動到元素並點擊
                self.driver.execute_script("arguments[0].scrollIntoView(true);", final_exam_menu)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", final_exam_menu)
                time.sleep(3)
                print("✅ 已點擊期末問卷選單")
            else:
                print("⚠️ 未找到期末問卷選單，嘗試直接導航")
                # 直接嘗試導航到問卷頁面
                self.driver.get("https://ceq.nkust.edu.tw/StuFillIn")
                time.sleep(3)
                
        except Exception as e:
            print(f"⚠️ 點擊期末問卷選單失敗: {e}")
        
        print("📝 步驟4: 尋找期末問卷填寫...")
        try:
            # 嘗試多種方式尋找期末問卷填寫
            fill_selectors = [
                "//a[contains(text(),'期末問卷填寫')]",
                "//span[contains(text(),'期末問卷填寫')]",
                "//div[contains(text(),'期末問卷填寫')]", 
                "//a[contains(text(),'問卷填寫')]",
                "//*[contains(text(),'期末問卷填寫')]"
            ]
            
            questionnaire_fill = None
            for selector in fill_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        questionnaire_fill = elements[0]
                        print(f"✅ 找到期末問卷填寫: {selector}")
                        break
                except:
                    continue
            
            if questionnaire_fill:
                # 滾動到元素並點擊
                self.driver.execute_script("arguments[0].scrollIntoView(true);", questionnaire_fill)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", questionnaire_fill)
                time.sleep(3)
                print("✅ 已進入期末問卷填寫頁面")
            else:
                print("⚠️ 未找到期末問卷填寫，可能已在正確頁面")
                
        except Exception as e:
            print(f"⚠️ 點擊期末問卷填寫失敗: {e}")
            print("可能已在正確頁面")
        
    def get_questionnaire_buttons(self):
        """步驟5: 獲取所有科目的填寫問卷按鈕"""
        print("\n🔍 步驟5: 尋找各科的填寫問卷按鈕...")
        
        # 確保在正確的頁面上
        try:
            if "StuFillIn" not in self.driver.current_url:
                print("⚠️ 不在問卷頁面，重新導航...")
                # 回到主頁重新導航
                self.driver.get("https://ceq.nkust.edu.tw/StuFillIn")
                time.sleep(2)
                # 重新執行導航步驟
                self.navigate_to_questionnaire_list()
        except Exception as nav_error:
            print(f"⚠️ 導航檢查失敗: {nav_error}")
        
        # 等待頁面載入完成
        time.sleep(3)
        
        questionnaire_buttons = []
        
        # 根據測試結果，按鈕是 input/button 元素，類別為 'btn btn-info'，文字為 '填寫問卷(Start)'
        print("🎯 使用正確的按鈕搜尋方法...")
        
        try:
            # 方法1: 直接尋找 btn btn-info 類別的按鈕
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn.btn-info")
            if buttons:
                for btn in buttons:
                    try:
                        btn_text = btn.text.strip() or btn.get_attribute('value') or ''
                        if "填寫問卷" in btn_text and "Start" in btn_text:
                            questionnaire_buttons.append(btn)
                    except:
                        continue
                print(f"✅ 找到 {len(questionnaire_buttons)} 個 btn-info 按鈕")
            
            # 方法2: 尋找包含 '填寫問卷(Start)' 文字的按鈕
            if not questionnaire_buttons:
                button_selectors = [
                    "button",
                    "input[type='button']", 
                    "input[type='submit']",
                    "a"
                ]
                
                for selector in button_selectors:
                    elements = self.driver.find_elements(By.TAG_NAME, selector.split('[')[0])
                    for element in elements:
                        try:
                            text = element.text.strip() or element.get_attribute('value') or ''
                            if text == "填寫問卷(Start)":
                                questionnaire_buttons.append(element)
                        except:
                            continue
                
                if questionnaire_buttons:
                    print(f"✅ 找到 {len(questionnaire_buttons)} 個匹配文字的按鈕")
            
            # 方法3: 通過表格結構尋找
            if not questionnaire_buttons:
                print("📊 通過表格結構搜尋...")
                tables = self.driver.find_elements(By.TAG_NAME, "table")
                for table in tables:
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        for cell in cells:
                            # 在每個cell中尋找按鈕
                            cell_buttons = cell.find_elements(By.TAG_NAME, "button")
                            cell_inputs = cell.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit']")
                            cell_links = cell.find_elements(By.TAG_NAME, "a")
                            
                            all_cell_elements = cell_buttons + cell_inputs + cell_links
                            
                            for element in all_cell_elements:
                                try:
                                    text = element.text.strip() or element.get_attribute('value') or ''
                                    if "填寫問卷" in text and "Start" in text:
                                        questionnaire_buttons.append(element)
                                except:
                                    continue
                
                if questionnaire_buttons:
                    print(f"✅ 表格搜尋找到 {len(questionnaire_buttons)} 個按鈕")
        
        except Exception as e:
            print(f"❌ 搜尋過程發生錯誤: {e}")
        
        # 去除重複的按鈕
        unique_buttons = []
        for button in questionnaire_buttons:
            if button not in unique_buttons:
                unique_buttons.append(button)
        
        print(f"\n📊 總共找到 {len(unique_buttons)} 個問卷按鈕")
        
        # 顯示找到的按鈕詳細資訊
        for i, btn in enumerate(unique_buttons):
            try:
                btn_text = btn.text.strip() or btn.get_attribute('value') or ''
                btn_tag = btn.tag_name
                btn_class = btn.get_attribute('class')
                btn_onclick = btn.get_attribute('onclick')
                print(f"   按鈕 {i+1}: '{btn_text}' (標籤: {btn_tag})")
                print(f"         類別: {btn_class}")
                print(f"         點擊: {btn_onclick}")
                print()
            except Exception as e:
                print(f"   按鈕 {i+1}: 無法讀取資訊 - {e}")
        
        return unique_buttons
        
    def fill_single_questionnaire(self):
        """步驟6: 填寫單一問卷"""
        print("🎲 開始填寫問卷...")
        time.sleep(2)
        
        # 1. 處理單選按鈕
        radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        radio_questions = {}
        
        for radio in radio_buttons:
            name = radio.get_attribute('name')
            if name:
                if name not in radio_questions:
                    radio_questions[name] = []
                radio_questions[name].append(radio)
        
        print(f"📊 發現 {len(radio_questions)} 個單選題")
        
        # 填寫單選題（偏向正面答案）
        radio_filled_count = 0
        for question_name, options in radio_questions.items():
            try:
                # 選擇偏向正面的答案（通常是後面的選項）
                if len(options) >= 4:
                    selected = random.choice(options[-3:])  # 選擇後3個選項之一
                else:
                    selected = random.choice(options)
                
                self.driver.execute_script("arguments[0].click();", selected)
                radio_filled_count += 1
                time.sleep(0.3)  # 避免操作過快
                
            except Exception as e:
                print(f"⚠️ 填寫單選題 {question_name} 失敗: {e}")
                continue
        
        # 2. 處理複選題（勾選題）- 特別注意8-1題
        checkbox_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        checkbox_questions = {}
        
        for checkbox in checkbox_buttons:
            name = checkbox.get_attribute('name')
            if name:
                if name not in checkbox_questions:
                    checkbox_questions[name] = []
                checkbox_questions[name].append(checkbox)
        
        print(f"✅ 發現 {len(checkbox_questions)} 個複選題（勾選題）")
        
        # 填寫複選題
        checkbox_filled_count = 0
        for question_name, options in checkbox_questions.items():
            try:
                print(f"🔲 處理複選題: {question_name}")
                
                # 特別處理8-1題或類似的問題
                if "8-1" in question_name or "8_1" in question_name or len(options) > 1:
                    # 對於複選題，隨機選擇1-3個選項
                    num_to_select = random.randint(1, min(3, len(options)))
                    selected_options = random.sample(options, num_to_select)
                    
                    for selected in selected_options:
                        if selected.is_displayed() and selected.is_enabled():
                            self.driver.execute_script("arguments[0].click();", selected)
                            time.sleep(0.2)
                    
                    print(f"   ✅ 已勾選 {num_to_select} 個選項")
                else:
                    # 單一複選框，直接勾選
                    if options[0].is_displayed() and options[0].is_enabled():
                        self.driver.execute_script("arguments[0].click();", options[0])
                        print(f"   ✅ 已勾選")
                
                checkbox_filled_count += 1
                
            except Exception as e:
                print(f"⚠️ 填寫複選題 {question_name} 失敗: {e}")
                continue
        
        # 3. 處理下拉選單
        select_elements = self.driver.find_elements(By.TAG_NAME, "select")
        select_filled_count = 0
        
        if select_elements:
            print(f"📋 發現 {len(select_elements)} 個下拉選單")
            
            from selenium.webdriver.support.ui import Select
            for i, select_element in enumerate(select_elements):
                try:
                    select = Select(select_element)
                    options = select.options
                    
                    # 跳過第一個選項（通常是"請選擇"），選擇正面的選項
                    if len(options) > 1:
                        # 偏向選擇後面的選項（通常是正面答案）
                        if len(options) >= 4:
                            selected_option = random.choice(options[-3:])
                        else:
                            selected_option = random.choice(options[1:])  # 跳過第一個
                        
                        select.select_by_index(options.index(selected_option))
                        select_filled_count += 1
                        time.sleep(0.3)
                        
                except Exception as e:
                    print(f"⚠️ 填寫下拉選單 {i+1} 失敗: {e}")
                    continue
        
        # 4. 填寫文字評論和必填欄位
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 
            "textarea, input[type='text']:not([name*='UserAccount']):not([name*='Password'])")
        
        text_filled_count = 0
        if text_inputs:
            print(f"✏️ 發現 {len(text_inputs)} 個文字輸入框...")
            
            # 擴充評論庫，確保有足夠的正面評論
            comments = [
                "課程內容豐富，受益良多。",
                "老師教學認真，講解清楚。", 
                "嗚啦呀哈~"
                "一袋米要扛幾袋樓!"
                "天上天下唯我獨尊"
                "我是一個小學生"
                "大不了輟學"
                "教授菜菜撈撈嗚嗚"
            ]
            
            for i, text_input in enumerate(text_inputs):
                try:
                    if text_input.is_displayed() and text_input.is_enabled():
                        # 檢查當前輸入框的內容
                        current_value = text_input.get_attribute('value') or text_input.text or ''
                        
                        # 檢查是否為必填欄位或空白欄位
                        should_fill = False
                        
                        # 情況1: 已經是空白的
                        if len(current_value.strip()) == 0:
                            should_fill = True
                        
                        # 情況2: 檢查父元素或相關元素是否有錯誤提示
                        try:
                            # 查找附近的錯誤訊息
                            parent = text_input.find_element(By.XPATH, "../..")
                            parent_text = parent.text.lower()
                            if any(keyword in parent_text for keyword in ['請填寫', '原因', '理由', '說明', 'required']):
                                should_fill = True
                        except:
                            pass
                        
                        # 情況3: 檢查是否有 required 屬性
                        if text_input.get_attribute('required'):
                            should_fill = True
                        
                        if should_fill:
                            text_input.clear()  # 清空現有內容
                            selected_comment = random.choice(comments)
                            text_input.send_keys(selected_comment)
                            text_filled_count += 1
                            print(f"   ✅ 已填寫文字框 {i+1}: {selected_comment}")
                        else:
                            print(f"   ⏭️ 跳過文字框 {i+1}: 已有內容且非必填")
                        
                        time.sleep(0.3)
                        
                except Exception as e:
                    print(f"⚠️ 處理文字輸入框 {i+1} 失敗: {e}")
                    # 即使出錯也嘗試填寫，確保不留空
                    try:
                        text_input.clear()
                        text_input.send_keys("課程很好，老師教學認真。")
                        text_filled_count += 1
                        print(f"   🔧 備用填寫完成")
                    except:
                        pass
                    continue
        
        total_filled = radio_filled_count + checkbox_filled_count + select_filled_count + text_filled_count
        print(f"\n✅ 問卷填寫完成！")
        print(f"   📊 單選題: {radio_filled_count} 個")
        print(f"   🔲 複選題: {checkbox_filled_count} 個") 
        print(f"   📋 下拉選單: {select_filled_count} 個")
        print(f"   ✏️ 文字評論: {text_filled_count} 個")
        print(f"   🎯 總計: {total_filled} 個項目")
    
    def final_check_required_fields(self):
        """提交前最後檢查所有必填欄位"""
        try:
            # 檢查所有空白的文字輸入框
            empty_text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 
                "textarea:not([readonly]), input[type='text']:not([readonly]):not([name*='UserAccount']):not([name*='Password'])")
            
            filled_count = 0
            for text_input in empty_text_inputs:
                try:
                    if text_input.is_displayed() and text_input.is_enabled():
                        current_value = text_input.get_attribute('value') or text_input.text or ''
                        if len(current_value.strip()) == 0:
                            # 發現空白欄位，填寫它
                            text_input.clear()
                            text_input.send_keys("課程內容充實，教學品質良好。")
                            filled_count += 1
                            print(f"🔧 補填空白欄位: 已填寫")
                            time.sleep(0.2)
                except:
                    continue
            
            # 檢查未選擇的單選題
            radio_groups = {}
            radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            
            for radio in radio_buttons:
                name = radio.get_attribute('name')
                if name:
                    if name not in radio_groups:
                        radio_groups[name] = []
                    radio_groups[name].append(radio)
            
            for group_name, buttons in radio_groups.items():
                try:
                    # 檢查這個群組是否有選中的
                    selected = any(btn.is_selected() for btn in buttons if btn.is_displayed())
                    if not selected and buttons:
                        # 沒有選中任何選項，選擇一個正面的
                        suitable_button = None
                        for btn in buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                suitable_button = btn
                                break
                        
                        if suitable_button:
                            self.driver.execute_script("arguments[0].click();", suitable_button)
                            filled_count += 1
                            print(f"🔧 補選未選的單選題: {group_name}")
                            time.sleep(0.2)
                except:
                    continue
            
            if filled_count > 0:
                print(f"✅ 最後檢查完成，補填了 {filled_count} 個欄位")
            else:
                print("✅ 最後檢查完成，所有欄位都已填寫")
                
        except Exception as e:
            print(f"⚠️ 最後檢查時發生錯誤: {e}")
        
    def submit_questionnaire(self):
        """步驟7: 送出問卷"""
        print("\n📤 步驟7: 送出問卷...")
        
        # 提交前最後檢查 - 確保所有必填欄位都已填寫
        print("🔍 提交前最後檢查...")
        self.final_check_required_fields()
        
        # 滾動到頁面底部
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 尋找送出按鈕
        submit_selectors = [
            "//input[contains(@value,'送出')]",
            "//button[contains(text(),'送出')]",
            "//input[@type='submit']",
            "//button[@type='submit']"
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                submit_button = self.driver.find_element(By.XPATH, selector)
                if submit_button.is_displayed():
                    button_text = submit_button.text or submit_button.get_attribute('value')
                    print(f"🎯 找到送出按鈕: {button_text}")
                    break
            except:
                continue
        
        if not submit_button:
            print("❌ 找不到送出按鈕")
            return False
        
        # 點擊送出按鈕
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", submit_button)
        print("✅ 已點擊送出按鈕")
        
        # 等待送出完成
        time.sleep(3)
        return True
        
    def run(self):
        """執行完整流程"""
        try:
            print("🎯 NKUST 問卷自動填寫系統")
            print("=" * 50)
            print(f"📝 帳號: {config.STUDENT_ID}")
            print("📋 流程: 登入 → 主頁 → 期末問卷 → 期末問卷填寫 → 各科填寫問卷 → 送出")
            print("=" * 50)
            
            # 設定瀏覽器
            self.setup_browser()
            
            # 步驟 1: 登入
            self.login()
            
            # 步驟 2-4: 導航到問卷列表
            self.navigate_to_questionnaire_list()
            
            # 步驟 5-7: 處理所有問卷
            completed_count = 0
            max_attempts = 3  # 最大重試次數
            
            for attempt in range(max_attempts):
                try:
                    print(f"\n🔄 第 {attempt + 1} 次嘗試處理問卷...")
                    questionnaire_buttons = self.get_questionnaire_buttons()
                    
                    if not questionnaire_buttons:
                        print("🎉 所有問卷都已完成！")
                        break
                    
                    # 逐一處理每個問卷
                    current_processed = 0
                    for i in range(len(questionnaire_buttons)):
                        try:
                            # 每次都重新獲取按鈕列表避免 stale element
                            fresh_buttons = self.get_questionnaire_buttons()
                            
                            if i >= len(fresh_buttons):
                                print(f"⚠️ 按鈕 {i+1} 已不存在，可能已完成")
                                continue
                            
                            button = fresh_buttons[i]
                            print(f"\n📝 正在處理第 {i+1} 個問卷...")
                            
                            # 滾動到按鈕位置並點擊
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            time.sleep(1)
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(4)  # 增加等待時間
                            
                            # 填寫問卷
                            self.fill_single_questionnaire()
                            
                            # 送出問卷
                            if self.submit_questionnaire():
                                completed_count += 1
                                current_processed += 1
                                print(f"✅ 第 {i+1} 個問卷已完成")
                            
                            
                        except Exception as e:
                            error_msg = str(e)
                            print(f"❌ 處理第 {i+1} 個問卷時發生錯誤: {error_msg}")
                            
                            # 檢查是否是會話失效
                            if "invalid session id" in error_msg or "session deleted" in error_msg:
                                print("💥 瀏覽器會話失效，需要重新啟動")
                                raise Exception("瀏覽器會話失效")
                            
                            # 嘗試恢復到問卷列表
                            try:
                                self.driver.back()
                                time.sleep(2)
                            except:
                                self.navigate_to_questionnaire_list()
                            continue
                    
                    # 檢查是否還有未完成的問卷
                    remaining_buttons = self.get_questionnaire_buttons()
                    if not remaining_buttons:
                        print("🎉 所有問卷都已完成！")
                        break
                    
                    print(f"ℹ️ 本輪完成 {current_processed} 個問卷，還有 {len(remaining_buttons)} 個未完成")
                    
                except Exception as session_error:
                    if "invalid session id" in str(session_error) or "session deleted" in str(session_error):
                        print("💥 瀏覽器會話失效，程式結束")
                        break
                    else:
                        print(f"❌ 處理過程發生錯誤: {session_error}")
                        if attempt < max_attempts - 1:
                            print(f"🔄 將進行第 {attempt + 2} 次嘗試...")
                            time.sleep(5)
                        continue
            
            print(f"\n🎉 任務完成！總共處理了 {completed_count} 個問卷")
            
        except Exception as e:
            print(f"❌ 程式執行發生錯誤: {e}")
            
        finally:
            print("\n🔚 程式執行完成")
            print("⏳ 5秒後自動關閉瀏覽器...")
            
            # 倒數計時
            for i in range(5, 0, -1):
                print(f"⏰ {i}秒後關閉...")
                time.sleep(1)
            
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("🚪 瀏覽器已關閉")

def main():
    """主程式入口"""
    filler = QuestionnaireAutoFiller()
    filler.run()

if __name__ == "__main__":
    main() 