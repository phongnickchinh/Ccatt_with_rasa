from ClearContent import try_pull

#Thực hiện duyệt qua danh sách listTour-trongNuoc.txt

# Path: database/BrowserAll.py

with open("database/listTour-trongNuoc.txt", "r") as f:
    listTour = f.read().split("\n")

#duyệt qua từng tour trong listTour
#tạo các biến để lưu lỗi và số lượng tour đã pull thành công

i=0
success=0
error_in_get_basic_info=0
error_in_get_highlights=0
error_in_get_tour_detail=0
error_in_get_price_on_departure=0
error_in_get_price_detail=0
error_in_get_policy=0

for tour in listTour:
    print("Tour" +str(i+1) + ": " + tour)
    result = try_pull(tour)
    if result=="success":
        success+=1
        print("Success" + str(success))
    else:
        i+=1
        print( result[0])
        if "get_basic_info" in result[1]:
            error_in_get_basic_info+=1
        if "get_highlights" in result[1]:
            error_in_get_highlights+=1
        if "get_tour_detail" in result[1]:
            error_in_get_tour_detail+=1
        if "get_price_on_departure" in result[1]:
            error_in_get_price_on_departure+=1
        if "get_price_detail" in result[1]:
            error_in_get_price_detail+=1
        if "get_policy" in result[1]:
            error_in_get_policy+=1

    print("\n-----------------------------------------------------------------------------\n")

print("Tổng số tour đã pull thành công: " + str(success))
print("Số lỗi trong hàm get_basic_info: " + str(error_in_get_basic_info))
print("Số lỗi trong hàm get_highlights: " + str(error_in_get_highlights))
print("Số lỗi trong hàm get_tour_detail: " + str(error_in_get_tour_detail))
print("Số lỗi trong hàm get_price_on_departure: " + str(error_in_get_price_on_departure))
print("Số lỗi trong hàm get_price_detail: " + str(error_in_get_price_detail))
print("Số lỗi trong hàm get_policy: " + str(error_in_get_policy))


    
