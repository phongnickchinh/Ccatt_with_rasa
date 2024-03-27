
import requests
from bs4 import BeautifulSoup
import re

#lấy các thông tin cơ bản
def get_basic_info(div, bigDiv):
    try:
        table = div.find("table", class_="tlb-info-tour")
        row=table.find_all("tr")
        departure_place = row[0].find_all("td")[0].text.strip()
        length = row[0].find_all("td")[1].text.strip()

        #phương tiện được thể hiện bằng các hình vẽ img có title tương ứng trong hàng 1 cột 3
        td = row[0].find_all("td")[2]
        vehicle = []
        for img in td.find_all("img"):
            vehicle.append(img["title"])

        tour_id = bigDiv.find("span", class_="id-tour").text.strip()

        #dịch vụ mở rộng
        ul=div.find("ul", class_="list-extra-services")
        list_extra_service=[]
        for li in ul.find_all("li"):
            list_extra_service.append(li.text.strip())

        return departure_place, length, vehicle, tour_id, list_extra_service
    except Exception as e:
        print("Error in basic_info: " + str(e))
        return None, None, None, None, None

#lấy điểm nhấn hành trình
def get_highlights(div):
    try:
        highlights=[]
        single_box_excerpt = div.find("div", class_="single-box-excerpt")
        if single_box_excerpt.find("li")==None:
            highlights.append(single_box_excerpt.text.strip().replace("\xa0"," "))
        else:
            for li in single_box_excerpt.find_all("li"):
                highlights.append(li.text.strip().replace("\xa0"," "))

        if len(highlights)==0:
            return None
        return highlights
    
    except Exception as e:
        print("Error in highlights: " + str(e))
        return None

#lấy thông tin chi tiét tour
def get_tour_detail(div):
    try:
        array_tittle=div.find("a", id="a-title-program-tour-0").text.strip()
        array = div.find("div", class_="panel-collapse collapse in").text.strip().replace("\n","").replace("\n", "").replace("\xa0"," ")
        array = array.split("LƯU Ý")[0]
        return  array
    except Exception as e:
        print("Error in tour_detail: " + str(e))
        return None

#lấy bảng giá mỗi điểm khởi hành
def get_price_on_departure(div):
    try:
        array=[]
        table=div.find("table", class_="banggia")
        if table==None:
            return "No price_table found"
        #lâsy bảng này lưu vào mảng 2 chiều
        for tr in table.find_all("tr"):
            row=[]
            for td in tr.find_all("td"):
                row.append(td.text.strip().replace("\n","").replace("\t","").replace("\r","").replace("\xa0"," ").replace("  "," "))
            array.append(row)
        return array
    except Exception as e:
        print("Error in get_price_on_departure: " + str(e))
        return None
    
#lấy các chi tiết bảng giá
def get_price_detail(div):
    try:
        try:
            array=div.find("div", id="table-price-1").find_all(["ul","ol"])
            if len(array)==0:
                array="No price_detail found"
            else:
                for i in range(len(array)):
                    list_li=array[i].find_all("li")
                    array[i]=[x.text.replace("\r", "").replace("\t"," ").replace("\n","").replace("\xa0", " ").strip() for x in list_li if x.text != ""]
        except Exception as e:
            array.append(div.find("div", id="table-price-1").text.replace("\r", "").replace("\t"," ").replace("\n","").replace("\xa0", " ").strip() )


        noteArray = None
        #trong trường hợp từ lưu ý được ghi riêng ở thẻ p, sau đó là đến thẻ chứa nội dung lưu ý thì sử dụng findnextsibling
        #nếu từ lưu ý và note được ghi chung ở trong 1 thẻ p thì lấy luôn thẻ đó
        try:
            if(div.find("div", id="table-price-1").find(lambda tag: tag.name == 'p' and tag.text.strip() == 'Lưu ý:')!=None):
                noteArray = div.find("div", id="table-price-1").find(lambda tag: tag.name == 'p' and tag.text.strip() == 'Lưu ý:').findNextSibling().findChildren()
                noteArray = [x.text.replace("\r", "").replace("\t"," ").replace("\n","") for x in noteArray if x.text != ""]
            if(div.find("div", id="table-price-1").find(lambda tag: tag.name == 'p' and tag.text.strip() == 'Lưu ý:')==None):
                noteArray = div.find("div", id="table-price-1").find(lambda tag: tag.name == 'p' and 'Lưu ý' in tag.text.strip()).text.strip()
            return array, noteArray
        except Exception as e:
            noteArray="No note_list found"
            return array, noteArray
    except Exception as e:
        #print("Error in get_price_detail: " + str(e))
        return None, None
    
#quy định, điều khoản được xử lí riêng với từng tour riêng biệt
def get_policy(div):
    try:
        tour_rules_tag=div.find("div", id="tour-rule-2")
        #nếu số kí tự text trong thẻ quá ít thì không xử lí, trả về "not found policy" với cả 4 giá trị
        if len(tour_rules_tag.text.strip())<30:
            return "not found part", "not found part", "not found part", "not found part"
        policy_note=None #tìm thẻ QUY TRÌNH ĐĂNG KÝ TOUR, thẻ này có thể là p hoặc h3
        policy_register=None #thẻ chứa lưu ý khi đăng ký tour, thường là thẻ sau của thẻ sau của policy_note
        cancellation_fee=None #phí hủy tour
        policy_register_note=None # tìm thẻ có nội dung NHỮNG LƯU Ý KHÁC, thẻ này có thể là p hoặc h3

        tags = tour_rules_tag.find_all(["h3", "p"])
        for tag in tags:
            if "ĐĂNG KÝ TOUR" in tag.text:
                policy_register = tag.findNext("ul").find_all("li")
                policy_register = [x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_register]
                policy_register_note = tag.findNext("ul").findNext("p").text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ")
            note_keywords = ["LƯU Ý KHÁC", "GHI CHÚ"]
            if any(keyword in tag.text for keyword in note_keywords):
                policy_note = tag.findNext("ul").find_all("li")
                policy_note = [x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_note]
        if policy_register==None:
            policy_register="Unable to extract policy_register"
        if policy_register_note==None:
            policy_register_note="Unable to extract policy_register_note"
        if policy_note==None:
            policy_note="Unable to extract policy_note"

        #tìm thẻ chứa phí hủy tour thẻ này có chưa nội dung "phí huỷ" hoặc "khoản hủy tour"
            #có thể do lỗi hiển thị với các kí tự đặc biệt nên khi viết tay từ "Phí hủy" và "khoản hủy tour" thì không tìm được
            #nhưng khi copy từ trang web thì tìm thấy, ôi ảo ma quáaaa
        cancellation_keywords = ["Phí hủy", "khoản hủy tour", "chi phí theo qui định", "HỦY VÉ TOUR", "hủy vé:", "phạt tiền tour", "CHUYỂN/HỦY TOUR", "ĐIỀU KIỆN  HỦY TOUR","QUY ĐỊNH HUỶ VÉ:", "QUY ĐỊNH HỦY/HOÀN TOUR", "DỜI NGÀY VÀ HOÀN HỦY"]
        for p in tour_rules_tag.find_all(["p", "h3"]):
            if any(keyword.lower() in p.text.lower() for keyword in cancellation_keywords):
                cancellation_fee = p.findNext("ul").find_all("li")
                cancellation_fee = [x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in cancellation_fee]
        if cancellation_fee==None:
            cancellation_fee="Unable to extract cancellation_fee"

        #nếu hàm trả về 4 Unable thì ghi trực tiếp text của thẻ vào policy_note
        if policy_register=="Unable to extract policy_register" and policy_register_note=="Unable to extract policy_register_note" and policy_note=="Unable to extract policy_note" and cancellation_fee=="Unable to extract cancellation_fee":
            policy_note = tour_rules_tag.text.strip().replace("\t","").replace("\n"," ").replace("\xa0"," ").replace("\r"," ").replace("  "," ").replace("  "," ").split("Xem thêm")[0].strip()
        return policy_register, policy_register_note, cancellation_fee, policy_note
    except Exception as e:
        #print("policy not clear:"+str(e))
        return None, None, None, None




def pull_and_clean(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #thẻ h1 class title-tour
    title = soup.find("h1", class_="title-tour").text
    div = soup.find("div", class_="single-content")
    div_breadcrumb=soup.find_all("div", class_="breadcrumb")

    # location là một list chứa các thẻ span
    temp = div_breadcrumb[0].find_all("span")
    location =temp[4].text.strip()

    #lấy thông tin cơ bản
    departure_place, length, vehicle, tour_id, list_extra_service = get_basic_info(div,soup)

    #điểm nhấn hành trình
    highlights = get_highlights(div)

    #chi tiết lịch trình
    detail = get_tour_detail(div)

    #lấy bảng giá
    price_on_departure = get_price_on_departure(div)

    #lấy chi tiết giá bao gồm, note
    price_detail, note =get_price_detail(div)

    #quy định, điều khoản
    policy_register, policy_register_note, cancellation_fee, policy_note = get_policy(div)
    #print(policy_note, "\n", policy_register, "\n", policy_register_note, "\n", cancellation_fee)

    return title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_register, policy_register_note, policy_note, cancellation_fee


def try_pull(url):
    
    try:
        #kiểm tra xem hàm nào trả về None, thêm vào list return tên hàm đó
        list_return=[]
        title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_register, policy_register_note, policy_note, cancellation_fee = pull_and_clean(url)
        list_tour_info=[title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_register, policy_register_note, policy_note, cancellation_fee]
        
        #ghi log lỗi mỗi hàm
        if title==None or location==None or departure_place==None or length==None or vehicle==None or tour_id==None or list_extra_service==None:
            list_return.append("get_basic_info")
        if highlights==None:
            list_return.append("get_highlights")
        if detail==None:
            list_return.append("get_tour_detail")
        if price_on_departure==None:
            list_return.append("get_price_on_departure")
        if price_detail==None or note==None:
            list_return.append("get_price_detail")
        if policy_note==None or policy_register==None or policy_register_note==None or cancellation_fee==None:
            list_return.append("get_policy")

        if len(list_return)==0:
            return "success",list_tour_info
        else:
            return "mini fail", list_return

    except Exception as e:
        print(e)
        return "fail",None



url_P="https://www.vietnambooking.com/du-lich/tour-chua-ba-chau-doc-nui-cam-tinh-bien-1n1d.htm"
try_pull(url_P)




