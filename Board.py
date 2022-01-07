from Point import Point
from Player import Player
from Field import Field
import math

class Board(object):
    def __init__(self, size: int, player1: Player, player2: Player, starting_point: Point, board_length):
        self.fields = [[]]
        self._player1 = player1
        self._player2 = player2
        self.__field_size = size
        self.__starting_point = starting_point
        self.__board_length = board_length

    def generate_fields(self):
        self.fields = [[0 for x in range(self.__board_length)] for y in range(self.__board_length)]
        x_pos = self.__starting_point.x
        y_pos = self.__starting_point.y
        x_spacing = math.sqrt(3) * self.__field_size * 0.5
        y_spacing = self.__field_size * 0.75

        for y in range(self.__board_length):
            x_pos = self.__starting_point.x + y * x_spacing * 0.5
            y_pos = self.__starting_point.y + y * y_spacing
            for x in range(self.__board_length):
                self.fields[x][y] = Field(Point(x_pos, y_pos), self.__field_size, None)

                index = y * 11 + x
                if y == 0:
                    self.fields[x][y].start_players.append(self._player1)
                if y == 10:
                    self.fields[x][y].end_players.append(self._player1)
                if index % 11 == 0:
                    self.fields[x][y].start_players.append(self._player2)
                if (index + 1) % 11 == 0:
                    self.fields[x][y].end_players.append(self._player2)

                self.fields[x][y].neighbors = self.get_neighbors_indexes(index)
                # print(f"({x}, {y}) = {y * 11 + x}: {self.fields[x][y].neighbors} - start: {self.fields[x][y].start_players} | end: {self.fields[x][y].end_players}")
                x_pos += x_spacing

    def get_start_fields_indexes(self, player: Player):
        indexes = []

        for y in range(self.__board_length):
            for x in range(self.__board_length):
                if player in self.fields[x][y].start_players:
                    indexes.append(y * 11 + x)

        return indexes

    def get_field(self, index: int):
        y = math.floor(index / 11)
        x = index % 11

        return self.fields[x][y]

    def get_neighbors_indexes(self, current_index: int):
        indexes = []

        if current_index > 10:
            indexes.append(current_index - 11)
            if (current_index + 1) % 11 != 0:
                indexes.append(current_index - 10)

        if current_index > 0 and current_index % 11 != 0:
            indexes.append(current_index - 1)

        if (current_index + 1) % 11 != 0:
            indexes.append(current_index + 1)

        if current_index < 110:
            if current_index % 11 != 0:
                indexes.append(current_index + 10)
            indexes.append(current_index + 11)

        return indexes

    def draw_board(self, pygame, window):
        for x in range(len(self.fields)):
            for y in range(len(self.fields[x])):
                self.fields[y][x].draw_field(pygame, window)

    def field_clicked(self, mouse_position, player: Player, special_acces: bool, pygame, window):
        field = self.find_field(mouse_position)

        if field == None or field.player == player or (field.player != None and special_acces == False):
            return False

        field.set_player(player)
        return True

    def find_field (self, mouse_position):
        x_pos = mouse_position[0] - self.__starting_point.x
        y_pos = mouse_position[1] - self.__starting_point.y
        radius = self.__field_size / 2

        x = round((math.sqrt(3) / 3 * x_pos - 1.0 / 3 * y_pos) / radius)
        y = round((2.0 / 3 * y_pos) / radius)

        if 0 <= x and x < self.__board_length and 0 <= y and y < self.__board_length:
            return self.fields[x][y]
        return None
