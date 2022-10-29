from core_classes import Game

game = Game(
    players_file="players_test.json",
    events_file="events_test.json"
)

print(game.execute_game())
