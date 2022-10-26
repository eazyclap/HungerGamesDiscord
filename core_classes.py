import json
from random import choice, random, randint
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

    # GAME PROPERTIES PLAYERS AND EVENTS
    @property
    def players(self):
        return self._players

    @property
    def events(self):
        return self._events

    # Internal function to enroll player into the players list
    def _enroll_player(self, player: Tribute):
        self._players.append(player)

    # Internal function to aadd event into the events list
    def _load_events(self, source: dict):
        self._events = source.copy()

    # Method to load an event list from a json
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

    # Method to pull an event from the list
    def pull_event(self, _min: int = 6, _max: int = 12):
        min_events = _min
        max_events = _max
        pulled_events = []
        for _ in range(randint(min_events, max_events)):
            new_event = choice(self.events)
            # Decider -> Random number that will be compared with the base event probability
            # If the decider is less or equal to the probability the event will be pulled and executed
            decider = random()
            if decider <= new_event.probability:
                pulled_events.append(new_event)
    