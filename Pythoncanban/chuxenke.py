def xen_ke(chuoi):
    ket_qua = ''
    for i, c in enumerate(chuoi):
        ket_qua += c.upper() if i % 2 == 0 else c.lower()
    return ket_qua

chuoi = input("Nhập vào chuỗi: ")
print(xen_ke(chuoi))