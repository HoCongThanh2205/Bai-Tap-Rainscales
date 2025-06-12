from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")

wait = WebDriverWait(driver, 10)
data_all = {}

# Lấy dữ liệu 4 trang
for page_num in range(1, 5):
    # Đợi bảng dữ liệu xuất hiện
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody tr")))

    # Thu thập dữ liệu của trang hiện tại
    rows = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr")
    data = []
    for row in rows:
        try:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                mst = cols[1].text.strip()
                name = cols[2].text.strip()
                date = cols[3].text.strip()
                data.append({"Tên doanh nghiệp": name, "Mã số thuế": mst, "Ngày cấp": date})
        except:
            continue

    df = pd.DataFrame(data)
    data_all[f"Trang_{page_num}"] = df

    # Nếu chưa tới trang cuối thì nhấn sang trang kế
    if page_num < 4:
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="pagination"]//a[@aria-label="{page_num+1}"]')))
        driver.execute_script("arguments[0].click();", next_page)  # dùng JS click để tránh lỗi scroll
        time.sleep(1)  # chờ một chút để dữ liệu tải lại

# Ghi ra file Excel với mỗi trang là một sheet
with pd.ExcelWriter("masothue.xlsx") as writer:
    for sheet_name, df in data_all.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

driver.quit()

print("Đã lưu file Excel: masothue.xlsx")
