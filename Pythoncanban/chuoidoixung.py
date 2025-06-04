def doi_xung(chuoi):
    return chuoi == chuoi[::-1]

chuoi = input("Nhập vào chuỗi: ")
print(doi_xung(chuoi))