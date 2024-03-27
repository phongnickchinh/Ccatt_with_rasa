from ClearContent import try_pull
import pymongo
import CheckLogFail
#tạo kết nối với database mongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["project2"]
mycol = mydb["tour_infor_2"]
print(myclient.list_database_names())


#chuyển độ dài tour từ dạng string sang dạng dict
def  convert_length_to_dict(string_length):
    #tring độ dài tour có dang "3 ngày 2 đêm" cần chuyển thành dạng dict {"day":3, "night":2}, cso thế có tour chỉ có ngày hoặc chỉ có đêm
    list_length = string_length.split(" ")
    dict_length = {}
    for i in range(len(list_length)):
        if list_length[i].isdigit():
            if list_length[i+1]=="ngày":
                dict_length["day"] = int(list_length[i])
            if list_length[i+1]=="đêm":
                dict_length["night"] = int(list_length[i])
    return dict_length
#tìm các ngày khởi hành của tour
def find_departure_date(list_banggia):
    departure_date = []
    try:
        for i in range(1, len(list_banggia)):
            if list_banggia[i][0]!="":
                departure_date.append(list_banggia[i][0])
    except:
        
        for i in range(len(list_banggia)):
            departure_date.append("null")
    return departure_date
#[[], ['', 'NGƯỜI LỚN(10 tuổi trở lên)', 'TRẺ EM(5 - 9 tuổi)', 'EM BÉ(1 - 4 Tuổi)'], ['Hàng ngày', '5,490,000 VND', 'Liên hệ', 'Liên hệ'], ['Từ Mùng 2 - Mùng 6', '6,250,000 VND', 'Liên hệ', 'Liên hệ']]
def find_price_on_departure(depaa, list_banggia):
    try:
        price_on_departure = []
        keys=list_banggia[1]
        #mỗi departure_date tương ứng với một hàng trong list_banggia, lưu thông tin giá với ngày khởi hành tương ứng
        for i in range(1, len(list_banggia)):
            if list_banggia[i][0]!="":
                price = {}
                for j in range(1, len(list_banggia[i])):
                    price[keys[j]] = list_banggia[i][j]
                price_on_departure.append(price)

        return price_on_departure
    except:
        #thêm "liên hệ" làm giá trị mặc định nếu không tìm thấy giá
        price_on_departure = []
        for i in range(len(depaa)):
            price_on_departure.append({"Giá":"Liên hệ"})
        return price_on_departure

#hàm chính
def browser():
    print("Start browser")
    with open("database/listTour-nuocNgoai.txt", "r") as f:
        listTour = f.read().split("\n")
    i, success = 0, 0
    error_in_get_basic_info, error_in_get_highlights, error_in_get_tour_detail = 0, 0, 0
    error_in_get_price_on_departure, error_in_get_price_detail, error_in_get_policy = 0, 0, 0
    #Clean các log trước đó

    with open("database/log_success.txt", "w") as f:
        f.write("")
    with open("database/log_fail.txt", "w") as f:
        f.write("")

    #duyệt qua từng tour trong listTour: 
    for tour in listTour:
        #in thứ tự tour đang xử lí
        print("Tour ", i+1, ": ", tour)
        check,list_result = try_pull(tour)

        if check=="success":
            print("Success")
            i+=1
            #xử lí các dữ liệu từ list_result đưa và database :title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_register, policy_register_note, policy_note, cancellation_fee
            title = list_result[0]
            location = list_result[1]
            departure_place = list_result[2]
            length = convert_length_to_dict(list_result[3])
            departure_date=find_departure_date(list_result[9])
            vehicle = list_result[4]
            tour_id = list_result[5]
            list_extra_service = list_result[6]
            highlights = list_result[7]
            detail = list_result[8]
            temp = find_price_on_departure(departure_date, list_result[9])
            price_on_departure = []
            for j in range(len(departure_date)):
                price_on_departure.append({departure_date[j]: temp[j]})
            print(price_on_departure)
            print("---------------------------------------------------------\n")
            price_detail = list_result[10]
            note = list_result[11]
            policy_register = list_result[12]
            policy_register_note = list_result[13]
            policy_note = list_result[14]
            cancellation_fee = list_result[15]
            #đưa các dữ liệu vào database
            mydict = {"title": title, "location": location, "departure_place": departure_place, "length": length, "vehicle": vehicle, "tour_id": tour_id, "list_extra_service": list_extra_service, "highlights": highlights, "detail": detail, "price_on_departure": price_on_departure, "price_detail": price_detail, "note": note, "policy_register": policy_register, "policy_register_note": policy_register_note, "policy_note": policy_note, "cancellation_fee": cancellation_fee}
            x = mycol.insert_one(mydict)
            success+=1
 
        if check=="mini fail":
            i+=1
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

    CheckLogFail.check_log_fail()

browser()
    
