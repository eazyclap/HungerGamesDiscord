import json
import pandas as pd
from core_classes import ArenaEvent


class EventManager:
    """
    This is an application written to simplify the creation of the events.json file.
    The create_from_csv() method allows to dump a json file compatible for the core_classes.Game class.
    !! WHEN LOADING A CSV MAKE SURE THAT ALL THE FLOATING POINT NUMBERS USE THE 0.00 FORMAT INSTEAD OF THE 0,00 !!
    """
    def __init__(self):
        self.created_events = []

    def _create_event(self, event_id: int, description: str, probability: float, tributes_involved: int, severity: int):
        new_event = ArenaEvent(
            id=event_id,
            description=description,
            probability=probability,
            tributes_involved=tributes_involved,
            severity=severity
        )
        self.created_events.append(new_event)

    def _dump(self, destination_filepath):
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

    def create_from_csv(self, filepath, destination_path):
        df = pd.read_csv(filepath)
        for row in range(len(df)):
            self._create_event(
                event_id=df["id"][row],
                description=df["description"][row],
                probability=df["probability"][row],
                tributes_involved=df["tributes_involved"][row],
                severity=df["severity"][row]
            )

        self._dump(destination_path)
