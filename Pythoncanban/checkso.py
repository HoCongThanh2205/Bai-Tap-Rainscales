def tach_so(chuoi):
    so = [int(c) for c in chuoi if c.isdigit()]
    return so if so else "Không có chữ số nào."

chuoi = input("Nhập vào chuỗi: ")
print(tach_so(chuoi))