
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
        array=div.find("div", id="table-price-1").find_all(["ul","ol"])
        if len(array)==0:
            array=None
        else:
            for i in range(len(array)):
                list_li=array[i].find_all("li")
                array[i]=[x.text.replace("\r", "").replace("\t"," ").replace("\n","").replace("\xa0", " ").strip() for x in list_li if x.text != ""]


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
        policy_note=None #tìm thẻ QUY TRÌNH ĐĂNG KÝ TOUR, thẻ này có thể là p hoặc h3
        policy_register=None #thẻ chứa lưu ý khi đăng ký tour, thường là thẻ sau của thẻ sau của policy_note
        cancellation_fee=None #phí hủy tour
        policy_register_note=None # tìm thẻ có nội dung NHỮNG LƯU Ý KHÁC, thẻ này có thể là p hoặc h3

        if tour_rules_tag.find("h3")!=None:
            #tim thẻ h3 có chứa nội dung QUY TRÌNH ĐĂNG KÝ TOUR
            for h3 in tour_rules_tag.find_all("h3"):
                if "ĐĂNG KÝ TOUR" in h3.text:
                    policy_register=h3.findNext ("ul").find_all("li")
                    policy_register=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_register]
                    policy_register_note=h3.findNext("ul").findNext("p").text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ")
                if "LƯU Ý KHÁC" in h3.text:
                    policy_note=h3.findNext("ul").find_all("li")
                    policy_note=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_note]
        else:
            #tim thẻ p có chứa nội dung QUY TRÌNH ĐĂNG KÝ TOUR
            for p in tour_rules_tag.find_all("p"):
                if "ĐĂNG KÝ TOUR" in p.text:
                    policy_register=p.findNext("ul").find_all("li")
                    policy_register=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_register]
                    policy_register_note=p.findNext("ul").findNext("p").text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ")
                if "LƯU Ý KHÁC" in p.text:
                    policy_note=p.findNext("ul").find_all("li")
                    policy_note=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in policy_note]

        #tìm thẻ chứa phí hủy tour thẻ này có chưa nội dung "phí huỷ" hoặc "khoản hủy tour"
        for p in tour_rules_tag.find_all("p"):
            #có thể do lỗi hiển thị với các kí tự đặc biệt nên khi viết tay từ "Phí hủy" và "khoản hủy tour" thì không tìm được
            #nhưng khi copy từ trang web thì tìm thấy, ôi ảo ma quáaaa
            if "Phí hủy" in p.text:
                print(p.text.strip())
                cancellation_fee=p.findNext("ul").find_all("li")
                cancellation_fee=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in cancellation_fee]
            if "khoản hủy tour" in p.text:
                print(p.text.strip())
                cancellation_fee=p.findNext("ul").find_all("li")
                cancellation_fee=[x.text.strip().replace("\t","").replace("\n","").replace("\xa0"," ").replace("\r"," ") for x in cancellation_fee]
        return policy_register, policy_register_note, cancellation_fee, policy_note
    except Exception as e:
        #print("policy not clear:"+str(e))
        return None, None, None, None




def pull_and_clean(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #thẻ h1 class title-tour
    title = soup.find("h1", class_="title-tour").text
    #print(title)
    div = soup.find("div", class_="single-content")
    div_breadcrumb=soup.find_all("div", class_="breadcrumb")

    # location là một list chứa các thẻ span
    temp = div_breadcrumb[0].find_all("span")
    location =temp[4].text.strip()
    #print(location)

    #lấy thông tin cơ bản
    departure_place, length, vehicle, tour_id, list_extra_service = get_basic_info(div,soup)

    #điểm nhấn hành trình
    highlights = get_highlights(div)
    #print(highlights)

    #chi tiết lịch trình
    detail = get_tour_detail(div)
    #print(detail)

    #lấy bảng giá
    price_on_departure = get_price_on_departure(div)
    #print(price_on_departure)
    #lấy chi tiết giá bao gồm, note
    price_detail, note =get_price_detail(div)
    # print(price_detail)
    # print(note)

    #quy định, điều khoản
    policy_register, policy_register_note, cancellation_fee, policy_note = get_policy(div)
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



url_P="https://www.vietnambooking.com/du-lich/tour-my-tho-1-ngay-cho-khach-doan.html"
try_pull(url_P)




