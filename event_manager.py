import json
import pandas as pd
from core_classes import ArenaEvent, Tribute


class EventManager:
    """
    This is an application written to simplify the creation of the events.json file.
    The create_from_csv() method allows to dump a json file compatible for the core_classes.Game class.
    !! WHEN LOADING A CSV MAKE SURE THAT ALL THE FLOATING POINT NUMBERS USE THE 0.00 FORMAT INSTEAD OF THE 0,00 !!

    This tool provides the possibility to auto-create these json files from a csv
    This allows to create all the necessary data with Google Sheets or Microsoft Excel
    
    The json files should respect the following structure:

    EVENTS FILE

    {
        "events": [
            {
                "id":...,
                "description":...,
                "probability":...,
                "tributes involved":...,
                "severity":...,
            },
            ...
        ]
    }


    PLAYERS FILE

    {
        "players": [
            {
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
    def _create_event(self, event_id: int, description: str, probability: float, tributes_involved: int, severity: int):
        new_event = ArenaEvent(
            id=event_id,
            description=description,
            probability=probability,
            tributes_involved=tributes_involved,
            severity=severity
        )
        self.created_events.append(new_event)

    def _create_player(self, name: str, district: str, hp: int, alive: bool):
        new_player = Tribute(
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
                "id": int(event.id),
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
                "name": str(tribute.name),
                "district": str(tribute.district),
                "hp": int(tribute.hp),
                "alive": bool(tribute.alive)
            })

        with open(destination_filepath, mode="w") as file:
            json.dump(output, file, indent=4)

    # Method to create an event json file from csv
    def create_event_from_csv(self, filepath, destination_path):
        df = pd.read_csv(filepath)
        for row in range(len(df)):
            self._create_event(
                event_id=df["id"][row],
                description=df["description"][row],
                probability=df["probability"][row],
                tributes_involved=df["tributes_involved"][row],
                severity=df["severity"][row]
            )

        self._dump_events(destination_path)

    # Method to create a player json file from csv
    def create_player_from_csv(self, filepath, destination_path):
        df = pd.read_csv(filepath)
        for row in range(len(df)):
            self._create_player(
                name=df["name"][row],
                district=df["district"][row],
                hp=df["hp"][row],
                alive=df["alive"][row]
            )

        self._dump_players(destination_path)
