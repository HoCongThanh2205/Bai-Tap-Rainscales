import pandas as pd
import numpy as np

input_nv_dict = {
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
}

input_pb_dict = {
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
}

df_nhanvien = pd.DataFrame(input_nv_dict)
df_phongban = pd.DataFrame(input_pb_dict)

print("Danh sách nhân viên:\n", df_nhanvien)
print("\n Danh sách phòng ban:\n", df_phongban)

print("\n Danh sách nhân viên có dữ liệu bị thiếu:\n", df_nhanvien.isnull())

df_nhanvien = df_nhanvien[df_nhanvien.isnull().sum(axis=1) <= 2]
print("\n Danh sách nhân viên sau khi xóa bớt hàng bị thiếu:\n", df_nhanvien)

df_nhanvien['Name'] = df_nhanvien['Name'].fillna('Chưa rõ')
df_nhanvien['Age'] = df_nhanvien['Age'].fillna(df_nhanvien['Age'].mean())
df_nhanvien['Salary'] = df_nhanvien['Salary'].ffill()
df_nhanvien['Department'] = df_nhanvien['Department'].fillna('Unknown')
print("\n Danh sách nhân viên sau khi thêm dữ liệu:\n", df_nhanvien)

df_nhanvien['Age'] = df_nhanvien['Age'].astype(int)
df_nhanvien['Salary'] = df_nhanvien['Salary'].astype(int)
print("\n Danh sách nhân viên đã đổi kiểu:\n", df_nhanvien)

df_nhanvien['Salary_after_tax'] = df_nhanvien['Salary'] * 0.9
print("\n Danh sách nhân viên có lương sau thuế:\n", df_nhanvien)

df_IT_25 = df_nhanvien[(df_nhanvien['Department'] == 'IT') & (df_nhanvien['Age'] > 25)]
print("\n Nhân viên phòng IT và có tuổi > 25:\n", df_IT_25)

df_sap_xep_luong = df_nhanvien.sort_values(by='Salary_after_tax', ascending=False)
print("\n Nhân viên sắp xếp theo lương sau thuế:\n", df_sap_xep_luong)

df_luong_tb = df_nhanvien.groupby('Department')['Salary'].mean().reset_index()
df_luong_tb.rename(columns={'Salary': 'Avg_salary'}, inplace=True)
print("\n Lương trung bình theo phòng ban:\n", df_luong_tb)

df_noi_nv_pb = pd.merge(df_nhanvien, df_phongban, on='Department', how='left')
print("\n Nhân viên và quản lý phòng ban:\n", df_noi_nv_pb)

input_nv_new_dict = {
    'ID': [107, 108],
    'Name': ['Thành', 'Phước'],
    'Age': [31, 29],
    'Department': ['IT', 'Marketing'],
    'Salary': [730, 740]
}

df_nhanvien_new = pd.DataFrame(input_nv_new_dict)
df_nhanvien_new['Salary_after_tax'] = df_nhanvien_new['Salary'] * 0.9
df_new = pd.concat([df_nhanvien, df_nhanvien_new], ignore_index=True)
print("\nBảng nhân viên đã được cập nhật:\n", df_new)
