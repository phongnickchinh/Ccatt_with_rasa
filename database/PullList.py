# Mục tiêu: lấy danh sách các tour từ website vietnambooking.com
import requests
import bs4
from bs4 import BeautifulSoup

url = "https://www.vietnambooking.com/du-lich-trong-nuoc.html"
#tìm thẻ a chứa link đến các tour dựa theo div có class="category-list-tour category-box-list-default category-box-sidebar-default"
def get_tour_link(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.contents)
    div = soup.find("div", class_="category-list-tour category-box-list-default category-box-sidebar-default")
    list_tour = []
    for h3 in div.find_all("h3", class_="title-h3"):
        a = h3.find("a")
        list_tour.append(a["href"])
        #print(a.text)

# #tạo và ghi vào file listTour.txt
#     with open("listTour.txt", "a") as file:
#         for tour in list_tour:
#             file.write(tour + "\n")
    
                    

#llặp 77 lần
for i in range(2):
    URL= url + "/" + str(i)
    get_tour_link(URL)