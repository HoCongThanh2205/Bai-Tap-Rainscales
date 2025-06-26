import os
import time
import xml.etree.ElementTree as ET
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook, load_workbook

# Cấu hình trình duyệt
def setup_driver(download_dir):
    os.makedirs(download_dir, exist_ok=True)
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=options)
    return driver, WebDriverWait(driver, 10)

# Tra cứu và tải XML
def tra_cuu_va_tai_xml(driver, wait, mst, mtc, url, download_dir):
    driver.get(url)
    domain = urlparse(url).netloc

    try:
        if "fpt.com.vn" in domain:
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MST bên bán']"))).send_keys(mst)
            driver.find_element(By.XPATH, "//input[@placeholder='Mã tra cứu hóa đơn']").send_keys(mtc)
            driver.find_element(By.XPATH,"//button[contains(@class, 'webix_button') and contains(text(), 'Tra cứu')]").click()
            time.sleep(2)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, "//button[span[contains(@class, 'mdi-xml')] and contains(text(), 'Tải XML')]").click()
            time.sleep(0.1)

        elif "meinvoice.vn" in domain:
            wait.until(EC.presence_of_element_located((By.NAME, "txtCode"))).send_keys(mtc)
            driver.find_element(By.ID, "btnSearchInvoice").click()
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, "download").click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "txt-download-xml").click()

        elif "ehoadon.vn" in domain:
            wait.until(EC.presence_of_element_located((By.ID, "txtInvoiceCode"))).send_keys(mtc)
            driver.find_element(By.CLASS_NAME, "btnSearch").click()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frameViewInvoice")))
            time.sleep(2)
            driver.find_element(By.ID, "btnDownload").click()
            time.sleep(1)
            driver.execute_script("document.querySelector('#divDownloads .dropdown-menu').style.display='block';")
            driver.find_element(By.ID, "LinkDownXML").click()

        else:
            print(f"Không hỗ trợ URL: {url}")
            return None 
        
        # Chờ file XML xuất hiện
        start_time = time.time()
        timeout = 20
        while time.time() - start_time < timeout:
            files = [f for f in os.listdir(download_dir) if f.endswith(".xml")]
            if files:
                files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
                return os.path.join(download_dir, files[0])
            time.sleep(1)

    except Exception as e:
        print(f"Lỗi khi xử lý {url}: {e}")
    return None

# Đọc dữ liệu từ XML
def read_xml_info(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Tìm node chính
        hdon_node = root.find(".//HDon")
        invoice_node = hdon_node.find("DLHDon") if hdon_node is not None else None
        if invoice_node is None:
            for tag in [".//DLHDon", ".//TDiep", ".//Invoice"]:
                node = root.find(tag)
                if node is not None:
                    invoice_node = node
                    break
            else:
                return None  # Không tìm thấy node chính

        def find(path):
            current = invoice_node
            for part in path.split("/"):
                if current is not None:
                    current = current.find(part)
                else:
                    return None
            return current.text if current is not None else None

        # Tìm số tài khoản bán
        stk_ban = find("NDHDon/NBan/STKNHang")
        if not stk_ban:
            for thongtin in invoice_node.findall(".//NBan/TTKhac/TTin"):
                if thongtin.findtext("TTruong") == "SellerBankAccount":
                    stk_ban = thongtin.findtext("DLieu")
                    break

        return {
            'Số hóa đơn': find("TTChung/SHDon"),
            'Đơn vị bán hàng': find("NDHDon/NBan/Ten"),
            'Mã số thuế bán': find("NDHDon/NBan/MST"),
            'Địa chỉ bán': find("NDHDon/NBan/DChi"),
            'Số tài khoản bán': stk_ban,
            'Họ tên người mua hàng': find("NDHDon/NMua/Ten"),
            'Địa chỉ mua': find("NDHDon/NMua/DChi"),
            'Mã số thuế mua': find("NDHDon/NMua/MST"),
        }
    except Exception as e:
        print(f"Lỗi đọc XML: {e}")
        return None

# Ghi dữ liệu ra Excel
def write_excel(filepath, data):
    if not os.path.exists(filepath):
        wb = Workbook()
        ws = wb.active
        ws.append([
            "STT", "MST", "Mã tra cứu", "URL",
            "Số hóa đơn", "Đơn vị bán hàng", "Mã số thuế bán", "Địa chỉ bán", "Số tài khoản bán",
            "Họ tên người mua hàng", "Địa chỉ mua", "Mã số thuế mua", "Ghi chú"
        ])
    else:
        wb = load_workbook(filepath)
        ws = wb.active
    for row in data:
        ws.append(row)
    wb.save(filepath)

# Hàm chính
def main():
    input_file = "input.xlsx"
    output_file = "output.xlsx"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(script_dir,"down_invoices")

    driver, wait = setup_driver(download_dir)
    df = pd.read_excel(input_file, dtype=str)
    result_rows = []

    for i, row in df.iterrows():
        mst = str(row.get("Mã số thuế", "")).strip()
        mtc = str(row.get("Mã tra cứu", "")).strip()
        url = str(row.get("URL", "")).strip()
        print(f"\n>> Đang xử lý: {mtc} | Trang: {url}")
        xml_file = tra_cuu_va_tai_xml(driver, wait, mst, mtc, url, download_dir)

        if xml_file:
            info = read_xml_info(xml_file)
            if info:
                result_rows.append([
                    i + 1, mst, mtc, url,
                    info["Số hóa đơn"], info["Đơn vị bán hàng"], 
                    info["Mã số thuế bán"], info["Địa chỉ bán"], 
                    info["Số tài khoản bán"],info["Họ tên người mua hàng"], 
                    info["Địa chỉ mua"], info["Mã số thuế mua"], ""
                ])
            else:
                result_rows.append([i + 1, mst, mtc, url] + [""] * 9 + ["Không đọc được XML"])
        else:
            result_rows.append([i + 1, mst, mtc, url] + [""] * 9 + ["Tải XML thất bại"])

    write_excel(output_file, result_rows)
    time.sleep(5)
    driver.quit()
    print(f"\n==> Đã lưu kết quả vào: {output_file}")

if __name__ == "__main__":
    main()
