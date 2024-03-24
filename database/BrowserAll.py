from ClearContent import try_pull

#Thực hiện duyệt qua danh sách listTour-trongNuoc.txt
# Path: database/BrowserAll.py
with open("database/listTour-trongNuoc.txt", "r") as f:
    listTour = f.read().split("\n")

#duyệt qua từng tour trong listTour
#tạo các biến để lưu lỗi và số lượng tour đã pull thành công
#hàm try_pull sẽ trả về 1 trong 3 trường hợp:
#- "success": pull thành công kèm theo list_result: title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_register, policy_register_note, policy_note, cancellation_fee
#- "mini fail": pull không thành công ở 1 trong 6 hàm: get_basic_info, get_highlights, get_tour_detail, get_price_on_departure, get_price_detail, get_policy
#- "fail": pull không thành công ở hàm pull_and_clean
i, success = 0, 0
error_in_get_basic_info, error_in_get_highlights, error_in_get_tour_detail = 0, 0, 0
error_in_get_price_on_departure, error_in_get_price_detail, error_in_get_policy = 0, 0, 0
#Clean các log trước đó
with open("database/log_success.txt", "w") as f:
    f.write("")
with open("database/log_fail.txt", "w") as f:
    f.write("")

#duyệt qua từng tour trong listTour
for tour in listTour:
    with open("database/log_success.txt", "a", encoding="utf-8") as f:
        i+=1
        check,list_result = try_pull(tour)
        if check=="success":
            success+=1
            #ghi lại list_result của tour thành công vào file log_success
            f.write("Tour "+str(i)+": "+tour+"\n")
            f.write("Title: "+str(list_result[0])+"\n")
            f.write("Location: "+str(list_result[1])+"\n")
            f.write("Departure place: "+str(list_result[2])+"\n")
            f.write("Length: "+str(list_result[3])+"\n")
            f.write("Vehicle: "+str(list_result[4])+"\n")
            f.write("Tour ID: "+str(list_result[5])+"\n")
            f.write("List extra service: "+str(list_result[6])+"\n")
            f.write("Highlights: "+str(list_result[7])+"\n")
            f.write("Detail: "+str(list_result[8])+"\n")
            f.write("Price on departure: "+str(list_result[9])+"\n")
            f.write("Price detail: "+str(list_result[10])+"\n")
            f.write("Note: "+str(list_result[11])+"\n")
            f.write("Policy register: "+str(list_result[12])+"\n")
            f.write("Policy register note: "+str(list_result[13])+"\n")
            f.write("Policy note: "+str(list_result[14])+"\n")
            f.write("Cancellation fee: "+str(list_result[15])+"\n")
            f.write("\n")
            f.write("------------------------------------------------------------------------------\n")
            
        if check=="mini fail":
            #ghi lại list_result của tour không thành công vào file log_fail
            with open("database/log_fail.txt", "a", encoding="utf-8") as f:
                f.write("Tour "+str(i)+": "+tour+"\n")
                f.write("Error in: "+str(list_result)+"\n")
                f.write("\n")
            if "get_basic_info" in list_result:
                error_in_get_basic_info+=1
            if "get_highlights" in list_result:
                error_in_get_highlights+=1
            if "get_tour_detail" in list_result:
                error_in_get_tour_detail+=1
            if "get_price_on_departure" in list_result:
                error_in_get_price_on_departure+=1
            if "get_price_detail" in list_result:
                error_in_get_price_detail+=1
            if "get_policy" in list_result:
                error_in_get_policy+=1
        if check=="fail":
            with open("database/log_fail.txt", "a", encoding="utf-8") as f:
                f.write("Tour "+str(i)+": "+tour+"\n")
                f.write("Error in: pull_and_clean\n")
                f.write("---------------------------------------------------------\n")

print("Success: ", success)
print("Error in get_basic_info: ", error_in_get_basic_info)
print("Error in get_highlights: ", error_in_get_highlights)
print("Error in get_tour_detail: ", error_in_get_tour_detail)
print("Error in get_price_on_departure: ", error_in_get_price_on_departure)
print("Error in get_price_detail: ", error_in_get_price_detail)
print("Error in get_policy: ", error_in_get_policy)

with open("database/log_success.txt", "a",encoding="utf-8") as f:
    f.write("Success: "+str(success)+"\n")
with open("database/log_fail.txt", "a", encoding="utf-8") as f:
    f.write("Error in get_basic_info: "+str(error_in_get_basic_info)+"\n")
    f.write("Error in get_highlights: "+str(error_in_get_highlights)+"\n")
    f.write("Error in get_tour_detail: "+str(error_in_get_tour_detail)+"\n")
    f.write("Error in get_price_on_departure: "+str(error_in_get_price_on_departure)+"\n")
    f.write("Error in get_price_detail: "+str(error_in_get_price_detail)+"\n")
    f.write("Error in get_policy: "+str(error_in_get_policy)+"\n")
    f.write("\n")


    
