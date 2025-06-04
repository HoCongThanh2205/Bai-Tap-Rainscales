def dem_ky_tu(chuoi):
    dem = {}
    for c in chuoi:
        dem[c] = dem.get(c, 0) + 1
    return dem

chuoi = input("Nhập vào chuỗi: ")
print(dem_ky_tu(chuoi))