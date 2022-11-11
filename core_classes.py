import json
from random import choice, random, randint
from dataclasses import dataclass


@dataclass
class ArenaEvent:
    """
    - description:........description of the event.
    - probability:........probability of the event (from 0% to 100%, 0.01 to 1.00).
    - tributes_involved:..number of tributes involved into the event.
    - severity:...........severity of the event, represents the number of the hp (health points) removed from the player
    ......................check list below for more details


    SEVERITY OF EVENTS:
    - 0:..........Information...........(eg: Tribute eats an apple)
    - 1 to 30:....Light event...........(eg: Tribute gets a light cut)
    - 31 to 70:...Medium event..........(eg: Tribute sprain an ankle)
    - 71 to 100:..Severe event..........(eg: Tribute dies)
    """

    description: str
    probability: float
    tributes_involved: int
    severity: int


@dataclass
class Tribute:
    """"
    - id:.................unique player ID code.
    - name:...............name of the tribute
    - district:...........district of the tribute, can be any name or number (realism is up to the game master)
    - hp:.................health points
    - alive:..............status of the tribute [alive/dead]
    """

    id: int
    name: str
    district: str
    hp: float = 100
    alive: bool = True


class Game:
    """
    Hunger Games class
    This is the basic class that contains the core game functions

    When started, the game class can be initialized with some data (given at the first class call) to resume an existing
    game.
    If no data is given, the game will be initialized blank and will wait for a load of event and players
    This can be done using the import_events_from_json() and import_players_from_json() methods

    The tool provided in the event_manager.py file provides the possibility to auto-create these json files from a csv
    This allows to create all the necessary data with applications like Google Sheets or Microsoft Excel
    Check event_manager.py for a detailed description.
    """

    def __init__(self, **kwargs) -> None:
        self._players = []
        self._events = []

        try:
            self.import_players_from_json(kwargs["players_file"])
        except KeyError:
            pass

        try:
            self.import_events_from_json(kwargs["events_file"])
        except KeyError:
            pass

    # GAME PROPERTIES PLAYERS AND EVENTS
    @property
    def players(self):
        return self._players

    @property
    def events(self):
        return self._events

    @property
    def alive_players(self):
        alive = []
        for player in self.players:
            if player.alive:
                alive.append(player)
        return alive

    @property
    def game_size(self):
        return len(self.players)

    # Internal function to enroll player into the players list (that contains the events data in dict form)
    def _enroll_player(self, player: Tribute) -> None:
        self._players.append(player)

    # Internal function to load evens from a list
    def _load_events(self, source: list) -> None:
        for item in source:
            new_event = ArenaEvent(
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
                id=item["id"],
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
                except KeyError:
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

    # Game execution
    def execute_game(self, minimum_events: int = 8, max_events: int = 12):
        # Working with copy of players and saving everything else at the end

        pulled_events = []

        # TEMPORARY STORAGE OF PLAYERS DATA
        players_cache = {}
        for player in self.alive_players:
            players_cache[player.id] = player

        def local_alive():
            local_alive_players = []
            for player in list(players_cache.values()):
                if player.alive:
                    local_alive_players.append(player)
            return local_alive_players

        def _understand_event(event: ArenaEvent):
            event_actives = event.description.count("#TRIBUTE")
            event_passives = event.description.count("#OPPRESSED")
            return event_actives, event_passives

        def _get_event_players(event: ArenaEvent):
            actives, passives = _understand_event(event)

            event_active_players = []
            event_passive_players = []

            # If not enough alive players the event can't be executed
            if actives + passives > len(local_alive()):
                return [], []

            # PASSIVE PLAYERS EXTRACTION
            while len(event_passive_players) < passives:
                new_player = choice(local_alive())
                event_passive_players.append(new_player)

            # ACTIVE PLAYERS EXTRACTION
            while len(event_active_players) < actives:
                new_player = choice(local_alive())
                while new_player in event_active_players or new_player in event_passive_players:
                    new_player = choice(local_alive())
                event_active_players.append(new_player)

            return event_active_players, event_passive_players

        for _ in range(randint(minimum_events, max_events)):
            new_event = choice(self.events)
            active_players, passive_players = _get_event_players(new_event)

            if not active_players or not passive_players:
                continue

            # Decider -> Random number that will be compared with the base event probability
            # If the decider is less or equal to the probability the event will be pulled and executed
            decider = random()
            if decider <= new_event.probability:
                pulled_events.append(
                    {
                        "event": new_event.description,
                        "active": active_players,
                        "passive": passive_players
                    }
                )
                for player in passive_players:
                    player.hp -= new_event.severity
                    if player.hp < 0:
                        player.hp = 0
                        player.alive = False
                    players_cache[player.id] = player

        for event in pulled_events:
            for i in range(len(event["active"])):
                event["event"] = event["event"].replace("#TRIBUTE", event["active"][i].name, i + 1)

            for i in range(len(event["passive"])):
                event["event"] = event["event"].replace("#OPPRESSED", event["passive"][i].name, i + 1)

        print(pulled_events)
        print(players_cache)
        return


if __name__ == "__main__":
    game = Game(
        players_file="./testing_files/players_test.json",
        events_file="./testing_files/events_test.json"
    )

    game.execute_game()
