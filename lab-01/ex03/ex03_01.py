def sum_so_chan(lst):
    sum = 0
    for num in lst:
        if num % 2 == 0:
            sum += num
    return sum

input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))

sum_chan = sum_so_chan(numbers)
print("Tổng các sỗ chẵn trong list là: ", sum_chan) 