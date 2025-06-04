def hoa_dau_tu(chuoi):
    return ' '.join([tu.capitalize() for tu in chuoi.split()])

chuoi = input("Nhập vào chuỗi: ")
print(hoa_dau_tu(chuoi))