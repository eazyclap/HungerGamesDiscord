import json
import pandas as pd
from core_classes import ArenaEvent, Tribute


class EventManager:
    """
    This is an application written to simplify the creation of the events.json and players.json files.
    The create_events_from_csv() and create_players_from_csv() methods allow to create a json file
    compatible for the core_classes.Game class.
    !! WHEN LOADING A CSV MAKE SURE THAT ALL THE FLOATING POINT NUMBERS USE THE 0.00 FORMAT INSTEAD OF THE 0,00 !!

    This tool provides the possibility to auto-create these json files from a csv.
    This allows to create all the necessary data with applications like Google Sheets or Microsoft Excel.
    
    The json files should respect the following structure:

    EVENTS FILE (Read below!)
    List that contains event proprieties in dictionary form

    {
        "events": [
            {
                "description":...,
                "probability":...,
                "tributes involved":...,
                "severity":...,
            },
            ...
        ]
    }

    Rules for events "description" parameter:
    - Event description should indicate the position of the players with the relative #TRIBUTE and #OPPRESSED keywords:
      These keywords specify who executes an action and/or who takes damage from it.
      Example 1: Tribute kills tribute.         --> #TRIBUTE kills #OPPRESSED.
      Example 2: Tribute dies from thirst.      --> #OPPRESSED gets a severe cut.
      Example 3: Tribute sings a song.          --> #TRIBUTE sings a song.
      Example 4: Tribute talks with tribute.    --> #TRIBUTE talks with #TRIBUTE.

    PLAYERS FILE
    List that contains player proprieties in dictionary form

    {
        "players": [
            {
                "id":...,
                "name":...,
                "district":...,
                "hp":...,
                "alive":...,    
            },
            ...
        ]
    }
    
    """

    def __init__(self):
        self.created_events = []
        self.created_players = []

    # INTERNAL FUNCTIONS TO LOAD AND EXPORT EVENTS/PLAYERS
    def _create_event(self, description: str, probability: float, tributes_involved: int, severity: int):
        new_event = ArenaEvent(
            description=description,
            probability=probability,
            tributes_involved=tributes_involved,
            severity=severity
        )
        self.created_events.append(new_event)

    def _create_player(self, player_id, name: str, district: str, hp: int, alive: bool):
        new_player = Tribute(
            id=player_id,
            name=name,
            district=district,
            hp=hp,
            alive=alive
        )
        self.created_players.append(new_player)
    
    def _dump_events(self, destination_filepath):
        output = {"events": []}

        for event in self.created_events:
            output["events"].append({
                "description": str(event.description),
                "probability": float(event.probability),
                "tributes involved": int(event.tributes_involved),
                "severity": int(event.severity)
            })

        with open(destination_filepath, mode="w") as file:
            json.dump(output, file, indent=4)

    def _dump_players(self, destination_filepath):
        output = {"players": []}

        for tribute in self.created_players:
            output["players"].append({
                "id": int(tribute.id),
                "name": str(tribute.name),
                "district": str(tribute.district),
                "hp": int(tribute.hp),
                "alive": bool(tribute.alive)
            })

        with open(destination_filepath, mode="w") as file:
            json.dump(output, file, indent=4)

    # Method to create an event json file from csv
    def create_events_from_csv(self, filepath, destination_path):
        df = pd.read_csv(filepath)
        for row in range(len(df)):
            self._create_event(
                description=df["description"][row],
                probability=df["probability"][row],
                tributes_involved=df["tributes_involved"][row],
                severity=df["severity"][row]
            )

        self._dump_events(destination_path)

    # Method to create a player json file from csv
    def create_players_from_csv(self, filepath, destination_path):
        df = pd.read_csv(filepath)
        for row in range(len(df)):
            self._create_player(
                player_id=df["id"][row],
                name=df["name"][row],
                district=df["district"][row],
                hp=df["hp"][row],
                alive=df["alive"][row]
            )

        self._dump_players(destination_path)
