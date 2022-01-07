from Board import Board
from Player import Player
from Field import Field

class SearchAlgorithm(object):
    def __init__(self, fields: [[]]):
        self._fields = fields
        self._visited = []
        self._to_visit = []

    def search(self, board: Board, player: Player):
        self._to_visit = board.get_start_fields_indexes(player)

        while any(self._to_visit):
            index = self._to_visit.pop()
            field = board.get_field(index)

            if index in self._visited or field.player != player:
                continue

            self._visited.append(index)

            if player in field.end_players:
                return True

            for neighbor in field.neighbors:
                self._to_visit.append(neighbor)

        return False
