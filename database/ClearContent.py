
import requests
from bs4 import BeautifulSoup

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
        array = div.find("div", class_="panel-collapse collapse in").text.strip().replace("\n","").replace("\xa0"," ")
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
        #quy trình đăng lý tour
        policy_register=tour_rules_tag.find(lambda tag: tag.name=='h3' and tag.text.strip()=='QUY TRÌNH ĐĂNG KÝ TOUR').findNextSibling().text.strip().replace("\r", "").replace("\t"," ").replace("\n","")
        policy_register_note=tour_rules_tag.find(lambda tag: tag.name=='h3' and tag.text.strip()=='QUY TRÌNH ĐĂNG KÝ TOUR').findNextSibling().findNextSibling().text.strip()
        #tìm kiếm thông tin LÀ THẺ ĐẰNG SAU thẻ h3 vào nôi dung chưa đoạn NHỮNG LƯU Ý KHÁC
        policy_note_tag=div.find("div", id="tour-rule-2").find(lambda tag: tag.name=='h3' and tag.text.strip()=='NHỮNG LƯU Ý KHÁC').findNextSibling().findChildren()
        policy_note=[x.text.strip().replace("\r", "").replace("\t"," ").replace("\n","") for x in policy_note_tag if x.text != ""]

        return policy_note, policy_register, policy_register_note
    except Exception as e:
        #print("policy not clear:"+str(e))
        return None, None, None




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
    policy_note, policy_register, policy_register_note = get_policy(div)
    return title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_note, policy_register, policy_register_note


def try_pull(url):
    
    try:
        #pull_and_clean(url_P)
        title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note,policy_note, policy_register, policy_register_note = pull_and_clean(url)
        #in ra tất cả
        # print("Title: ", title)
        # print("Location: ", location)
        # print("Departure Place: ", departure_place)
        # print("Length: ", length)
        # print("Vehicle: ", vehicle)
        # print("Tour ID: ", tour_id)
        # print("List Extra Service: ", list_extra_service)
        # print("Highlights: ", highlights)
        # print("Detail: ", detail)
        # print("Price on Departure: ", price_on_departure)
        # print("Price Detail: ", price_detail)
        # print("Note: ", note)
        # print("Policy Note: ", policy_note)
        # print("Policy Register: ", policy_register)
        # print("Policy Register Note: ", policy_register_note)

        #kiểm tra xem hàm nào trả về None, thêm vào list return tên hàm đó
        list_return=[]
        list_tour_info=[title, location, departure_place, length, vehicle, tour_id, list_extra_service, highlights, detail, price_on_departure, price_detail, note, policy_note, policy_register, policy_register_note]
        
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
        if policy_note==None or policy_register==None or policy_register_note==None:
            list_return.append("get_policy")

        if len(list_return)==0:
            return "success",list_tour_info
        else:
            return "mini fail", list_return

    except Exception as e:
        print(e)
        return "fail",None



url_P="https://www.vietnambooking.com/du-lich/tour-cao-bang-bac-kan-lang-son-3n2d.html"
print(url_P)
try_pull(url_P)




