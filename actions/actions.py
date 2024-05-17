# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
#kết nối database mongodb
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('localhost', 27017)

class tourSuggest(Action):
    def name(self) -> Text:
        return "action_tour_suggest"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("đã chạy action_tour_suggest")
        # Lấy giá trị của thực thể "season" từ tracker
        season = tracker.get_slot("season")

        #tìm kiếm các tour hấp dẫn theo mùa trogn project2.tour_info
        db = client.project2
        collection = db.tour_info
        #tìm trong tên tour nếu xuất hiện season thì trả về
        tours = collection.find({"title": {"$regex": season}})
        

        # Sau khi tìm kiếm, phản hồi với thông tin tìm được
        if(tours.count() == 0):
            dispatcher.utter_message(text=f"Không tìm thấy tour nào phù hợp với mùa {season}")
        else:
            dispatcher.utter_message(text=f"Trong {season} này, có các tour hấp dẫn sau: \n{tours}")

        return []



