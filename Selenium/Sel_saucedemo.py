from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Bỏ qua popups: cảnh báo, lưu mật khẩu, vv.
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# Danh sách tài khoản test
usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]
password = "secret_sauce"
url = "https://www.saucedemo.com/"

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

data_all_users = []

for username in usernames:
    driver.get(url)
    time.sleep(1)

    # Nhập username và password
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # Kiểm tra đăng nhập thành công bằng URL
    if "inventory" in driver.current_url:
        print(f"Đăng nhập thành công với {username}")
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
            data_all_users.append({
                "Username": username,
                "Product Name": name,
                "Price": price
            })
    else:
        print(f"Đăng nhập thất bại với {username}")

    # Quay lại trang login
    time.sleep(1)

# Đóng trình duyệt
driver.quit()

# Ghi dữ liệu vào Excel
df = pd.DataFrame(data_all_users)
df.to_excel("saucedemo_products.xlsx", index=False)
print("Đã lưu file Excel: saucedemo_products.xlsx")
