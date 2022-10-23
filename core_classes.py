import json
import requests
from dataclasses import dataclass


@dataclass
class ArenaEvent:
    """
    - id:.................unique event ID code.
    - description:........description of the event.
    - probability:........probability of the event (from 0% to 100%, 0.01 to 1.00).
    - tributes_involved:..number of tributes involved into the event.
    - severity:...........severity of the event, represents the number of the hp (health points) removed from the player.
    ......................check list below for more details


    SEVERITY OF EVENTS:
    - 0:..........Information...........(eg: Tribute eats an apple)
    - 1 to 30:....Light event...........(eg: Tribute gets a light cut)
    - 31 to 70:...Medium event..........(eg: Tribute sprain an ankle)
    - 71 to 100:..Severe event..........(eg: Tribute dies)
    """

    id: int
    description: str
    probability: float
    tributes_involved: int
    severity: int


@dataclass
class Tribute:
    """"
    - name: name of the tribute
    - district: district of the tribute, can be any name or number (realism is up to the game master)
    - hp: health points
    - alive: status of the tribute [alive/dead]
    """

    name: str
    district: str
    hp: float = 100
    alive: bool = True


class Game:
    def __init__(self):
        self._players = []
        self._events = []

    @property
    def players(self):
        return self._players

    @property
    def events(self):
        return self._events

    def enroll_player(self, player: Tribute):
        self._players.append(player)

    def _load_events(self, source: dict):
        self._events = source.copy()

    def load_from_json(self, source):
        if isinstance(source, str):
            try:
                with open(source, mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                pass
            else:
                try:
                    self._load_events(data["events"])
                except KeyError:
                    pass
        elif isinstance(source, dict):
            self._load_events(source)
