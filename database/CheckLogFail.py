#trong file log_fail được ghi lại với dạng sau:
# Tour 709: https://www.vietnambooking.com/du-lich/tour-du-lich-chau-doc-ha-tien-phu-quoc-5n4d-hang-thang.html
# Error in: ['get_price_detail', 'get_policy']
#hãy lấy ra url của tour bị lỗi

import re
import os

def check_log_fail():
    with open("database/log_fail.txt", "r", encoding="utf-8") as f:
        data = f.read()
        urls = re.findall(r"Tour \d+: (https://www.vietnambooking.com/du-lich/.*?.html)", data)
    #ghi lần lượt các url fail này vào listTour-trongNuoc.txt
        #xoá nội dung cũ
    with open("database/listTour-trongNuoc.txt", "w") as f:
        f.write("")
    #ghi url mới
    with open("database/listTour-trongNuoc.txt", "a") as f:
        for url in urls:
            f.write(url+"\n")
        