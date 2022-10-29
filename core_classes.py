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
    """
    Hunger Games class
    This is the basic class that contains the core game functions

    When started, the game class can be initialized with some data (given at the first class call) to resume an existing game
    If no data is given, the game will be initialized blank and will wait for a load of event and players
    This can be done using the import_events_from_json() and import_players_from_json() methods

    The tool provided in the event_manager.py file provides the possibility to auto-create these json files from a csv
    This allows to create all the necessary data with applications like Google Sheets or Microsoft Excel
    Check event_manager.py for a detailed description.
    """
    def __init__(self, **kwargs) -> None:
        self._players = []
        self._events = []

        if not kwargs["players_file"] is None:
            self.import_players_from_json(kwargs["players_file"])

        if not kwargs["events_file"] is None:
            self.import_events_from_json(kwargs["events_file"])
            
    # GAME PROPERTIES PLAYERS AND EVENTS
    @property
    def players(self):
        return self._players

    @property
    def events(self):
        return self._events

    # Internal function to enroll player into the players list (that contains the events data in dict form)
    def _enroll_player(self, player: Tribute) -> None:
        self._players.append(player)

    # Internal function to load evens from a list
    def _load_events(self, source: list) -> None:
        for item in source:
            new_event = ArenaEvent(
                id=item["id"],
                description=item["description"],
                probability=item["probability"],
                tributes_involved=item["tributes involved"],
                severity=item["severity"]
            )
            self._events.append(new_event)

    # Internal functions to load the players from a list (that contains the events data in dict form)
    def _load_players(self, source: list) -> None:
        for item in source:
            new_tribute = Tribute(
                name=item["name"],
                district=item["district"],
                hp=item["hp"],
                alive=item["alive"]
            )
            self._players.append(new_tribute)
                
    # Method to load an event list from a json
    def import_events_from_json(self, source) -> None:
        if isinstance(source, str):
            try:
                with open(source, mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                pass
            else:
                try:
                    self._load_events(data["events"])
                except KeyError as e:
                    pass
        elif isinstance(source, dict):
            self._load_events(source["events"])

    # Method to load players from a json
    def import_players_from_json(self, source) -> None:
        if isinstance(source, str):
            try:
                with open(source, mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                pass
            else:
                try:
                    self._load_players(data["players"])
                except KeyError:
                    pass
        elif isinstance(source, dict):
            self._load_players(source["players"])
            
    # Method to pull an event from the list
    def execute_game(self, minimum_events: int = 6, max_events: int = 12):
        # Internal function to extract players for an event, makes sure the same player is not extracted twice
        def _get_event_players(num: int) -> list:
            players = []
            for _ in range(num):
                new_player = choice(self.players)
                while new_player in players:
                    new_player = choice(self.players)
                players.append(new_player)
            return players

        # Pulled events list
        pulled_events = []
        event_players = []

        # In the selected range, pull the necessary events
        for _ in range(randint(minimum_events, max_events)):
            new_event = choice(self.events)
            # Decider -> Random number that will be compared with the base event probability
            # If the decider is less or equal to the probability the event will be pulled and executed
            decider = random()
            if decider <= new_event.probability:
                pulled_events.append(new_event)

        for event in pulled_events:
            players_needed = event.tributes_involved
            event_players = _get_event_players(players_needed)

        # TESTING PURPOSE - CONTINUE WITH EVENT EXECUTION AND SAVE RELEVANT DATA
        return f"{len(pulled_events)} events pulled!\n{pulled_events}"
