def cat_ho_ten(ho_ten):
    tu = ho_ten.strip().split()
    ho_lot = ' '.join(tu[:-1])
    ten = tu[-1]
    return ho_lot, ten

ho_ten = input("Nhập họ và tên: ")
print(cat_ho_ten(ho_ten))