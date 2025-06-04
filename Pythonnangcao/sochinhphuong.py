import math

def socp(n):
    can = int(math.sqrt(n))
    return can * can == n

def songuyen(sn):
    while True:
        try:
            so = int(input(sn))
            return so
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ.")

while True:
    a = songuyen("Nhập số nguyên a: ")
    b = songuyen("Nhập số nguyên b: ")
    if a < b:
        break
    else:
        print("Giá trị a phải nhỏ hơn b. Vui lòng nhập lại.")

ketqua = []
for i in range(a, b + 1):
    if i % 3 == 0 and not socp(i):
        ketqua.append(str(i))

print(", ".join(ketqua))