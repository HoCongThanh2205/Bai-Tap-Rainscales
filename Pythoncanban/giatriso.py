def gia_tri(so):
    hang_dv = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tram = so // 100
    chuc = (so % 100) // 10
    dv = so % 10

    ket_qua = f"{hang_dv[tram]} trăm"
    if chuc == 0 and dv != 0:
        ket_qua += " linh"
    elif chuc != 0:
        ket_qua += f" {hang_dv[chuc]} mươi"   
    if dv != 0:
        if dv == 5 and chuc != 0:
            ket_qua += " lăm"
        else:
            ket_qua += f" {hang_dv[dv]}"   
    return ket_qua.strip()

so = int(input("Nhập vào 1 số: "))
print(gia_tri(so))