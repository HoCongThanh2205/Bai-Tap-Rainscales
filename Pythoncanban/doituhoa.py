def chuyen_tu(chuoitu):
    tu = chuoitu.lower().split()
    tu_chuan = ' '.join([t.capitalize() for t in tu])
    return tu_chuan

chuoi = input("Nhập vào từ cần chuyển: ")
print(chuyen_tu(chuoi))