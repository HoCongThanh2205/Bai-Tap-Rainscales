def dao_nguoc_tu(chuoi):
    return ' '.join(chuoi.split()[::-1])

chuoi = input("Nhập vào chuỗi cần đảo: ")
print(dao_nguoc_tu(chuoi))