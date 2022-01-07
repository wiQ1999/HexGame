from Player import Player
from Board import Board
from Point import Point
from SearchAlgorithm import SearchAlgorithm
import pygame

class Game(object):
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((1280, 720))
        self._font_title = pygame.font.SysFont("Comic Sans MS", 50)
        self._font_header = pygame.font.SysFont("Comic Sans MS", 46)
        self._font_normal = pygame.font.SysFont("Comic Sans MS", 24)
        self._player1 = None
        self._player2 = None

    def game_start(self):
        while True:
            if self.set_players() == False:
                break
            if self.play() == False:
                break



    def play(self):
        board = Board(50, self._player1, self._player2, Point(90, 160), 11)
        board.generate_fields()

        current_player_tag = 1
        current_player = self._player1
        round = 1

        self.show_playboard(board, current_player, round)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    return True
                if event.type == pygame.MOUSEBUTTONUP:
                    special_acces = False
                    if round == 2:
                        special_acces = True

                    if board.field_clicked(pygame.mouse.get_pos(), current_player, special_acces, pygame, self.window):
                        if SearchAlgorithm(board.fields).search(board, current_player):
                            return self.show_winner_screen(current_player, round)

                        current_player_tag *= -1
                        if (current_player_tag == 1):
                            current_player = self._player1
                        else:
                            current_player = self._player2

                        self.show_playboard(board, current_player, round)

                        round += 1


    def show_winner_screen(self, winner: Player, rounds: int):
        self.window.fill((50, 50, 145))
        text_winner = self._font_title.render(f"{winner.name} wygrał w {rounds} ruchach!", False, "white")
        self.window.blit(text_winner, text_winner.get_rect(center=(1280 / 2, 100)))
        text_enter = self._font_normal.render("Kliknij, aby kontynuować", False, "white")
        self.window.blit(text_enter, text_enter.get_rect(center=(1280 / 2, 600)))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    return True

    def show_playboard(self, board: Board, current_player: Player, round: int):
        self.window.fill((50, 50, 145))
        pygame.draw.polygon(self.window, "darkblue", [(0, 0), (600, 0), (1000, 720), (0, 720)])

        pygame.draw.polygon(self.window, board._player1.color, [(40, 130), (415, 345), (555, 130)])
        pygame.draw.polygon(self.window, board._player1.color, [(288, 565), (415, 345), (790, 565)])
        pygame.draw.polygon(self.window, board._player2.color, [(40, 130), (415, 345), (288, 565)])
        pygame.draw.polygon(self.window, board._player2.color, [(790, 565), (415, 345), (555, 130)])

        board.draw_board(pygame, self.window)

        text_player_header = self._font_header.render("Tura gracza:", False, "white")
        self.window.blit(text_player_header, (700, 50))
        text_player = self._font_normal.render(current_player.name, False, current_player.color)
        self.window.blit(text_player, (1000, 70))

        text_rounds_header = self._font_header.render("Runda:", False, "white")
        self.window.blit(text_rounds_header, (750, 150))
        text_rounds = self._font_normal.render(str(round), False, current_player.color)
        self.window.blit(text_rounds, (920, 170))

        text_restart = self._font_normal.render("Esc, aby zrestartować:", False, "white")
        self.window.blit(text_restart, (1000, 600))

        pygame.display.update()

    def set_players(self):
        self.show_player_colors_options("Wybierz kolor pierwszego gracza:")
        color1 = self.choice_color()
        if (color1 == None):
            return False
        self._player1 = Player("Gracz1", color1, True)

        self.show_player_colors_options("Wybierz kolor drugiego gracza:", color1)
        color2 = self.choice_color(color1)
        if (color2 == None):
            return False
        self._player2 = Player("Gracz2", color2, False)

        return True

    def show_player_colors_options(self, header_text: str, missing_color = None):
        self.window.fill((50, 50, 145))

        text_header = self._font_header.render(header_text, False, "white")
        self.window.blit(text_header, text_header.get_rect(center=(1280 / 2, 100)))

        if missing_color != pygame.Color(255, 0, 0):
            text_color = self._font_normal.render("1)  red", False, "red")
            self.window.blit(text_color, (580, 160))
        if missing_color != pygame.Color(255, 255, 0):
            text_color = self._font_normal.render("2)  yellow", False, "yellow")
            self.window.blit(text_color, (580, 200))
        if missing_color != pygame.Color(0, 255, 0):
            text_color = self._font_normal.render("3)  green", False, "green")
            self.window.blit(text_color, (580, 240))
        if missing_color != pygame.Color(0, 255, 255):
            text_color = self._font_normal.render("4)  light blue", False, "light blue")
            self.window.blit(text_color, (580, 280))
        if missing_color != pygame.Color(255, 0, 255):
            text_color = self._font_normal.render("5)  pink", False, "pink")
            self.window.blit(text_color, (580, 320))

        pygame.display.update()

    def choice_color(self, missing = None):
        player_color = None
        while player_color == None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1 and missing != pygame.Color(255, 0, 0):
                        return pygame.Color(255, 0, 0)
                    if event.key == pygame.K_2 and missing != pygame.Color(255, 255, 0):
                        return pygame.Color(255, 255, 0)
                    if event.key == pygame.K_3 and missing != pygame.Color(0, 255, 0):
                        return pygame.Color(0, 255, 0)
                    if event.key == pygame.K_4 and missing != pygame.Color(0, 255, 255):
                        return pygame.Color(0, 255, 255)
                    if event.key == pygame.K_5 and missing != pygame.Color(255, 0, 255):
                        return pygame.Color(255, 0, 255)
        return player_color
