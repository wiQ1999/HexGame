import platform
from math import sin, cos, pi
from Point import Point
from Player import Player
import pygame
import random


class Field(object):
    def __init__(self, center: Point, size: int, player: Player):
        assert center.x >= 0, f"Wartość {center.x} na osi X nie może być mniejsza od 0"
        assert center.y >= 0, f"Wartość {center.y} na osi Y nie może być mniejsza od 0"
        assert size > 0, f"Promień o wartości {size} musi być większy od 0"

        self.center = center
        self.player = player
        self.neighbors = []
        self.start_players = []
        self.end_players = []
        self._size = size
        self._corners = self.__calculate_corners()

    def add_neighbors(self, indexes: []):
        self.neighbors = indexes

    def add_neighbors(self, players: []):
        self.winning_players = players

    def set_player(self, player: Player):
        self.player = player

    def set_player_and_draw(self, pygame, window, player):
        self.player = player
        self.draw_field(pygame, window)

    def draw_field(self, pygame, window):
        if self.player == None:
            pygame.draw.polygon(window, "gray", [(p.x, p.y) for p in self._corners])
            pygame.draw.polygon(window, "black", [(p.x, p.y) for p in self._corners], 2)
        else:
            pygame.draw.polygon(window, self.player.color, [(p.x, p.y) for p in self._corners])
            #pygame.draw.polygon(window, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [(p.x, p.y) for p in self._corners])
            pygame.draw.polygon(window, "black", [(p.x, p.y) for p in self._corners], 2)

    def __calculate_corners(self):
        corners = []
        size_radius = self._size * 0.5
        for i in range(6):
            degrees = 60 * i - 30 # ustawione czubato do góry
            radius = pi / 180 * degrees
            corners.append(Point(self.center.x + size_radius * cos(radius), self.center.y + size_radius * sin(radius)))
        return corners

    def __str__(self):
        return f"Field: {self.center}, {self.player}"
