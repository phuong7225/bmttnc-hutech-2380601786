def dao_nguoc_chuoi(chuoi):
    return chuoi[::-1]

nhap_chuoi = input("Nhập chuỗi cần đảo ngược: ")
print("Chuỗi đảo ngược là: ", dao_nguoc_chuoi(nhap_chuoi))