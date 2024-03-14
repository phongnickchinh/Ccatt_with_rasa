#từ file listTour.txt trong folder database chứa các đường dẫn đến các tour, lấy thông tin của các tour ghi vào file tourInfo.txt theo dạng json

import requests
from bs4 import BeautifulSoup
with open("database/listTour-trongNuoc.txt", "r") as file:
    list_tour = file.read().split("\n")
    list_tour.pop()
    print(list_tour)
    
    i=0
    for tour in list_tour:
        page = requests.get(tour)
        soup = BeautifulSoup(page.content, "html.parser")
        title =soup.find("h1", class_="title-tour")
        div = soup.find("div", class_="single-content")
        print(title.text)
        print(div)
        with open("database/tourInfo.txt", "a", encoding='utf-8') as file:
            file.write(title.text + "\n")
            file.write(div.text + "\n")
        i+=1
        if(i==2):
            break