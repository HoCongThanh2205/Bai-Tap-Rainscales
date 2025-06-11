from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Các tài khoản test có thể sử dụng
usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user"
]
password = "secret_sauce"
url = "https://www.saucedemo.com/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

all_data = []

for username in usernames:
    driver.get(url)
    time.sleep(1)
    
    # Điền tài khoản & mật khẩu
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # Kiểm tra login thành công
    if "inventory" in driver.current_url:
        # Lấy danh sách sản phẩm
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
            all_data.append({
                "username": username,
                "product_name": name,
                "price": price
            })
    
    # Logout (nếu cần) hoặc quay lại trang đăng nhập
    driver.get(url)
    time.sleep(1)

driver.quit()

# Lưu vào Excel
df = pd.DataFrame(all_data)
df.to_excel("saucedemo_products.xlsx", index=False)
print("Đã lưu danh sách sản phẩm.")
