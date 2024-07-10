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
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
#kết nối database mongodb
# from pymongo import MongoClient

# # Kết nối tới MongoDB
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['project2']
# collection = db['tour_infor']

# class ActionTourSuggestSeason(Action):
#     def name(self) -> str:
#         return "action_tour_suggest_season"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
#         season = next(tracker.get_latest_entity_values("season"), None)
#         if not season:
#             dispatcher.utter_message(text="Tôi không thể xác định được mùa bạn muốn đi du lịch. Vui lòng chỉ định rõ mùa.")
#             return []
#         # Example query: tìm tour theo mùa
#         query = {"title": {"$regex": season, "$options": "i"}}

#         try:
#             count = collection.count_documents(query)
#             dispatcher.utter_message(text=f"Found {count} tours for the summer season.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# #Xử lí action tìm tour theo ngân sách
# class ActionCustomerBudget(Action):
#     def name(self) -> str:
#         return "find_tour_by_budget"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
#         budget = next(tracker.get_latest_entity_values("budget"), None)

#         if not budget:
#             dispatcher.utter_message(text="Tôi không thể xác định được ngân sách của bạn. Vui lòng chỉ định rõ ngân sách.")
#             return []
#         # Example query: tìm ngân sách trong tên tour
#         query = {"title": {"$regex": budget, "$options": "i"}}
#         #tìm ngân sách trong tên tour


#         try:
#             count = collection.count_documents(query)
#             dispatcher.utter_message(text=f"Found {count} tours for the budget.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []

# #tìm 5 tour đầu tiên trong database
# class ActionTourSuggestGeneral(Action):
#     def name(self) -> str:
#         return "action_tour_suggest_general"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
#         # Example query: tìm 5 tour đầu tiên
#         query = {}

#         try:
#             tours = collection.find(query).limit(5)
#             for tour in tours:
#                 dispatcher.utter_message(text=f"Tour: {tour['title']}")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []

class ActionInformAdvise(Action):

    def name(self) -> Text:
        return "action_inform_advise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')
        phone_number = tracker.get_slot('phone_number')
        email = tracker.get_slot('email')
        tourid = tracker.get_slot('tourid')

        if name and phone_number and email and tourid:
            response = f"Here is the advice based on your information:\nName: {name}\nPhone Number: {phone_number}\nEmail: {email}"
        else:
            response = "I need more information to provide the advice."

        dispatcher.utter_message(text=response)

        return []
    