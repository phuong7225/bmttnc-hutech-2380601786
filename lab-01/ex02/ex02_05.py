so_gio_lam = float(input("Nhập số giờ làm mỗi tuần: "))
muc_luong_gio = float(input("Nhập mức lương tiêu chuẩn:"))

gio_tieu_chuan = 44
gio_OT = max (0, so_gio_lam - gio_tieu_chuan)

luong = gio_tieu_chuan * muc_luong_gio + gio_OT * muc_luong_gio * 1.5

print(f"Số tiền lương của nhân viên: {luong}")