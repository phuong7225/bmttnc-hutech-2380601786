def chia_het_cho_5(nhi_phan):
    #Chuyển Nhị phân -> Thập phân
    thap_phan = int(nhi_phan, 2)
    
    if thap_phan % 5 == 0:
        return True
    else:
        return False
chuoi_nhi_phan = input("Nhập chuỗi số nhị phân (phân tách bằng dấu phẩy): ")

nhi_phan_list = chuoi_nhi_phan.split(',')
so_chia_het_cho_5 = [so for so in nhi_phan_list if chia_het_cho_5(so)]

if len(so_chia_het_cho_5) > 0:
    kq = ','.join(so_chia_het_cho_5)
    print("Các số nhị phan chia hết cho 5 là: ", kq)
else:
    print("Không có số nào chia hết cho 5 trong chuỗi đã nhập.")