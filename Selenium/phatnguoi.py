from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytesseract
from PIL import Image
import os
import time
import base64

# Ẩn cảnh báo Tensorflow (nếu dùng chung môi trường)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def open_chrome():
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/")
    return driver

def xu_ly_bien_kiem_soat(driver, str_bien_so):
    xpath = '//*[@id="formBSX"]/div[2]/div[1]/input'
    driver.find_element(By.XPATH, xpath).send_keys(str_bien_so)

def xu_ly_loai_phuong_tien(driver, loai_phuong_tien):
    xpath_select = '//*[@id="formBSX"]/div[2]/div[2]/select'
    select_elem = driver.find_element(By.XPATH, xpath_select)
    select_elem.click()

    options_xpath = xpath_select + '/option'
    options = driver.find_elements(By.XPATH, options_xpath)
    for option in options:
        if option.text.strip() == loai_phuong_tien:
            option.click()
            time.sleep(1)
            break

def xu_ly_capcha(driver):
    captcha_element = driver.find_element(By.ID, "imgCaptcha")
    src = captcha_element.get_attribute("src")
    if "base64," in src:
        base64_data = src.split(",")[1]
        with open("captcha.png", "wb") as f:
            f.write(base64.b64decode(base64_data))
    else:
        captcha_element.screenshot("captcha.png")
    image = Image.open("captcha.png")
    captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3').strip()
    input_xpath = '//*[@id="formBSX"]/div[2]/div[3]/div/input'
    input_elem = driver.find_element(By.XPATH, input_xpath)
    input_elem.clear()
    input_elem.send_keys(captcha_text)
    print(f"[CAPTCHA]: {captcha_text}")

def tra_cuu_phat_nguoi(driver, bien_so, loai_phuong_tien):
    driver.get("https://www.csgt.vn/")
    time.sleep(1)

    xu_ly_bien_kiem_soat(driver, bien_so)
    xu_ly_loai_phuong_tien(driver, loai_phuong_tien)
    xu_ly_capcha(driver)

    tra_cuu_button_xpath = '//*[@id="formBSX"]/div[2]/input[1]'
    driver.find_element(By.XPATH, tra_cuu_button_xpath).click()

    try:
        ketqua = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ketqua"]'))
        )
        print(f"[Kết quả - {loai_phuong_tien}]: {ketqua.text}")
    except:
        print(f"[Không có kết quả - {loai_phuong_tien}]: CAPTCHA sai hoặc không có vi phạm.")

def main():
    driver = open_chrome()
    bien_so = "43A12345"
    for loai in ["Ô tô", "Xe máy", "Xe đạp điện"]:
        tra_cuu_phat_nguoi(driver, bien_so, loai)
        time.sleep(2)
    driver.quit()
main()
