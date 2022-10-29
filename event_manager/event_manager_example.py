"""
Example of the EventManager class
In this example I am creating the necessary JSON files (Used in the testing_files/execute_game_test.py) with the
EventManager methods create_players_from_csv() and create_events_from_csv()
"""

from event_manager import EventManager

manager = EventManager()
manager.create_players_from_csv("../testing_files/players_test.csv", "../testing_files/players_test.json")
manager.create_events_from_csv("../testing_files/events_test.csv", "../testing_files/events_test.json")
