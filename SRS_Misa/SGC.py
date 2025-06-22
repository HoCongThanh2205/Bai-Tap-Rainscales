import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

# Cấu hình
URL = "https://meinvoice.vn/tra-cuu"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "misa")
LOG_FILE = os.path.join(SCRIPT_DIR, "logs.txt")
INPUT_FILE = os.path.join(SCRIPT_DIR, "matracuu.txt")
WAIT_TIME = 15

# Đọc file mã tra cứu
def read_ma_tra_cuu():
    if INPUT_FILE.endswith(".txt"):
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    elif INPUT_FILE.endswith(".xlsx"):
        df = pd.read_excel(INPUT_FILE)
        return df.iloc[:, 0].dropna().astype(str).tolist()
    else:
        raise Exception("Chỉ đọc file .txt hoặc .xlsx")

# Ghi nhật ký tra cứu vào file log
def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# Thiết lập driver
def setup_driver():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

# Kiểm tra kết nối
def check_website_loaded(driver):
    try:
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "txtCode"))
        )
        return True
    except TimeoutException:
        write_log("Không thể tải trang meinvoice.vn - Kiểm tra kết nối internet.")
        return False

# Tra cứu hóa đơn
def tra_cuu_hoa_don(driver, ma_tra_cuu):
    try:
        driver.get(URL)
        if not check_website_loaded(driver):
            write_log(f"Mã '{ma_tra_cuu}': Không tải được trang.")
            return
        wait = WebDriverWait(driver, WAIT_TIME)

        # Nhập mã tra cứu
        input_box = wait.until(EC.presence_of_element_located((By.ID, "txtCode")))
        input_box.clear()
        input_box.send_keys(ma_tra_cuu)

        # Nhấn nút tra cứu
        search_btn = driver.find_element(By.ID, "btnSearchInvoice")
        search_btn.click()

        # Đợi kết quả hoặc lỗi hiện ra
        try:
            wait.until(EC.presence_of_element_located((By.ID, "showPopupInvoice")))
            write_log(f"Mã '{ma_tra_cuu}': Tìm thấy hóa đơn.")

            # Click nút "Tải hóa đơn" (span)
            try:
                btn_open_download = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "download-invoice"))
                )
                driver.execute_script("arguments[0].click();", btn_open_download)

                # Chờ menu hiện ra rồi click "Tải PDF"
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "txt-download-pdf")))
                pdf_btn = driver.find_element(By.CLASS_NAME, "txt-download-pdf")
                pdf_btn.click()
                time.sleep(3)
                write_log(f"Mã '{ma_tra_cuu}': Đã tải hóa đơn PDF.")
            except Exception as e:
                write_log(f"Mã '{ma_tra_cuu}': Không thể tải PDF: {str(e)}")
        except TimeoutException:
            write_log(f"Mã '{ma_tra_cuu}': Không tìm thấy hóa đơn.")
    except Exception as e:
        write_log(f"Mã '{ma_tra_cuu}': Lỗi khi tra cứu: {str(e)}")

def main():
    try:
        ma_tra_cuu_list = read_ma_tra_cuu()
        driver = setup_driver()
        for ma in ma_tra_cuu_list:
            tra_cuu_hoa_don(driver, ma)
            time.sleep(2)
        driver.quit()
        write_log("Hoàn tất quá trình tra cứu.")
    except Exception as e:
        write_log(f"Lỗi tổng quát: {str(e)}")
if __name__ == "__main__":
    main()
