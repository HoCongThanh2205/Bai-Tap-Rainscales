from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
time.sleep(3)

sheet_dict = {}
page_num = 1

while True:
    print(f"Đang thu thập trang {page_num}...")
    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3:
            name = cols[0].text.strip()
            tax_code = cols[1].text.strip()
            date = cols[2].text.strip()
            data.append({
                "Tên doanh nghiệp": name,
                "Mã số thuế": tax_code,
                "Ngày cấp": date
            })
    
    sheet_dict[f"Trang_{page_num}"] = pd.DataFrame(data)

    # Tìm nút "Trang sau"
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(., 'Trang sau')]")
        if "disabled" in next_btn.get_attribute("class"):
            break
        else:
            next_btn.click()
            time.sleep(2)
            page_num += 1
    except:
        break  # Không tìm thấy nút "Trang sau" => kết thúc

driver.quit()

# Ghi vào file Excel nhiều sheet
with pd.ExcelWriter("doanh_nghiep_mst.xlsx") as writer:
    for sheet, df in sheet_dict.items():
        df.to_excel(writer, sheet_name=sheet, index=False)

print("Đã lưu dữ liệu doanh nghiệp vào file Excel.")
