import pandas as pd

my_dict = {
    'Name': ['Nhân', 'Diện', 'Tài', 'Vinh', 'Thành', 'Dũng', 'Khoa', 'Tú', 'Hải', 'Đạt'],
    'Age': [20, 21, 22, 20, 23, 21, 22, 20, 24, 21],
    'Gender': ['Nam', 'Nữ', 'Nam', 'Nam', 'Nam', 'Nam', 'Nam', 'Nữ', 'Nam', 'Nam'],
    'Score': [6.5, 7.0, 4.5, 8.0, 5.5, 3.0, 9.0, 6.0, 7.5, 4.0]
}

df_students = pd.DataFrame(my_dict)
df_students.index = range(1, len(df_students) + 1)

print("Danh sách sinh viên:")
print(df_students)

print("\n3 sinh viên đầu tiên:")
print(df_students.head(3))

print("\nTên sinh viên tại index = 2:")
print(df_students.loc[2, 'Name'])

print("\nTuổi tại index = 10:")
print(df_students.loc[10, 'Age'])

print("\nCột Name và Score:")
print(df_students[['Name', 'Score']])

df_students['Pass'] = df_students['Score'] >= 5
print("\nDanh sách sau khi thêm cột 'Pass':")
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\nDanh sách sau khi sắp xếp theo Score giảm dần:")
print(df_sorted)