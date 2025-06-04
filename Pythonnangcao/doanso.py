import time

def randomso():
    miligiay = int(time.time() * 1000)  
    return miligiay % 999 + 1           

def nhap():
    while True:
        try:
            so = int(input("Nhập số bạn đoán (1–999): "))
            if 1 <= so <= 999:
                return so
            else:
                print("Số phải nằm trong khoảng 1–999.")
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ.")

def thoat():
    while True:
        traloi = input("Bạn có muốn thoát trò chơi không? (c/k): ").strip().lower()
        if traloi in ['c', 'k']:
            return traloi == 'c'
        else:
            print("Vui lòng nhập 'c' (có) hoặc 'k' (không).")

dapan = randomso()
sosai = 0

while True:
    doan = nhap()
    
    if doan == dapan:
        print(f"Bạn đã dự đoán chính xác số {dapan}!")
        break
    else:
        sosai += 1
        if abs(doan - dapan) <= 10:
            print("Bạn đoán gần đúng rồi!")
        else:
            print(f"Bạn đã trả lời sai {sosai} lần")

        if sosai >= 5:
            if thoat():
                print("Cảm ơn bạn đã chơi. Hẹn gặp lại!")
                break
            else:
                print("Bạn đoán trật tất cả năm lần, kết quả đã thay đổi. Mời bạn đoán lại.")
                dapan = randomso()
                sosai = 0