def tu_max(chuoi):
    max_char = max(chuoi, key=chuoi.count)
    return max_char, chuoi.count(max_char)

chuoi = input("Nhập vào chuỗi: ")
print(tu_max(chuoi))