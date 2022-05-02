import pygame
from Artificial_Intelligence import ArtificialIntelligence


COLOR_BLUE = (29, 52, 97)
COLOR_PINK = (176, 48, 136)
COLOR_FIELD = (255, 242, 204)
COLOR_LINES = (118, 118, 127)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
        self.actions = 1
        self.player = 1
        self.board[0][0] = 1
        self.winner = -1
        self.score = [0, 0, 0]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.draw_text(screen)
        cross1 = 0
        cross2 = 0
        square1 = 0
        square2 = 0
        for i in range(self.width):
            for j in range(self.height):
                x, y = self.left + i * self.cell_size, self.top + j * self.cell_size
                if self.board[i][j] == -1:
                    square1 += 1
                    pygame.draw.rect(screen, COLOR_BLUE, (x, y, self.cell_size, self.cell_size), 0)
                elif self.board[i][j] == -2:
                    square2 += 1
                    pygame.draw.rect(screen, COLOR_PINK, (x, y, self.cell_size, self.cell_size), 0)
                else:
                    if self.board[i][j] == 1:
                        cross1 += 1
                        self.draw_cross(screen, COLOR_BLUE, x, y, self.cell_size, 7)
                    elif self.board[i][j] == 2:
                        cross2 += 1
                        self.draw_cross(screen, COLOR_PINK, x, y, self.cell_size, 7)
                pygame.draw.rect(screen, COLOR_LINES, (x, y, self.cell_size, self.cell_size), 1)
        self.draw_game_score(screen, self.left + 450, self.top - 150, cross1, cross2, square1, square2)
        self.score[1] = cross1 + square1
        self.score[2] = cross2 + square2

    @staticmethod
    def draw_cross(screen, color, x, y, size, width):
        pygame.draw.line(screen, color, (x, y), (x + size, y + size), width)
        pygame.draw.line(screen, color, (x + size, y), (x, y + size), width)

    def draw_game_score(self, screen, x, y, cross1, cross2, square1, square2):
        scs = 40  # score_cell_size
        dist = 100
        pygame.draw.rect(screen, COLOR_BLUE, (x, y, scs, scs), 0)
        self.draw_cross(screen, COLOR_BLUE, x, y + scs + 10, scs, 7)
        pygame.draw.rect(screen, COLOR_LINES, (x, y, scs, scs), 2)
        pygame.draw.rect(screen, COLOR_LINES, (x, y + scs + 10, scs, scs), 2)
        pygame.draw.rect(screen, COLOR_PINK, (x + scs + dist, y, scs, scs), 0)
        self.draw_cross(screen, COLOR_PINK, x + scs + dist, y + scs + 10, scs, 7)
        pygame.draw.rect(screen, COLOR_LINES, (x + scs + dist, y, scs, scs), 2)
        pygame.draw.rect(screen, COLOR_LINES, (x + scs + dist, y + scs + 10, scs, scs), 2)
        font = pygame.font.Font(None, 70)
        text_blue_1 = font.render(str(square1), True, COLOR_BLUE)
        text_blue_2 = font.render(str(cross1), True, COLOR_BLUE)
        text_blue_3 = font.render(str(square1 + cross1), True, COLOR_BLUE)
        text_blue_4 = font.render("S", True, COLOR_BLUE)
        screen.blit(text_blue_1, (x + 60, y))
        screen.blit(text_blue_2, (x + 60, y + text_blue_1.get_height()))
        screen.blit(text_blue_3, (x + 60, y + text_blue_1.get_height() + text_blue_2.get_height()))
        screen.blit(text_blue_4, (x + 5, y + text_blue_1.get_height() + text_blue_2.get_height()))
        text_pink_1 = font.render(str(square2), True, COLOR_PINK)
        text_pink_2 = font.render(str(cross2), True, COLOR_PINK)
        text_pink_3 = font.render(str(square2 + cross2), True, COLOR_PINK)
        text_pink_4 = font.render("S", True, COLOR_PINK)
        screen.blit(text_pink_1, (x + scs + dist + 60, y))
        screen.blit(text_pink_2, (x + scs + dist + 60, y + text_pink_1.get_height()))
        screen.blit(text_pink_3, (x + scs + dist + 60, y + text_pink_1.get_height() + text_pink_2.get_height()))
        screen.blit(text_pink_4, (x + scs + dist + 5, y + text_pink_1.get_height() + text_pink_2.get_height()))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        if x < 0 or y < 0:
            return None
        x //= self.cell_size
        y //= self.cell_size
        if x >= self.width or y >= self.height:
            return None
        return x, y

    def check_move(self, i, j, visited, player):
        visited[i][j] = True
        if self.board[i][j] == player:
            return True
        for del_i in range(-1, 2, 1):
            for del_j in range(-1, 2, 1):
                if del_i != 0 or del_j != 0:
                    new_i = i + del_i
                    new_j = j + del_j
                    if 0 <= new_i < self.width and 0 <= new_j < self.height:
                        if not visited[new_i][new_j]:
                            if abs(self.board[new_i][new_j]) == player:
                                res = self.check_move(new_i, new_j, visited, player)
                                if res:
                                    return True
        return False

    def on_click(self, cell):
        i, j = cell[0], cell[1]
        visited = [[False] * self.height for _ in range(self.width)]
        if self.board[i][j] == 0:
            if self.check_move(i, j, visited, self.player):
                self.board[i][j] = self.player
                return True
            return False
        if self.board[i][j] < 0:
            return False
        if self.board[i][j] == self.player:
            return False
        if self.check_move(i, j, visited, self.player):
            self.board[i][j] = -self.player
            return True
        return False

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            if self.on_click(cell):
                self.actions += 1
                if self.actions % 3 == 0:
                    self.player = 3 - self.player
                if self.actions == 3:
                    self.actions += 1
                    self.board[self.width - 1][self.height - 1] = 2

    def get_move_ai(self):
        ai = ArtificialIntelligence(self.width, self.height, self.board, self.player, self.actions)
        res = ai.get_move()
        if res is not None:
            self.on_click(res)
            self.actions += 1
        if self.actions % 3 == 0:
            self.player = 3 - self.player

    def get_winner(self):
        if self.winner != -1:
            return self.winner
        if self.actions <= 6:
            return self.winner
        ai = ArtificialIntelligence(self.width, self.height, self.board, self.player, self.actions + 1)
        res = ai.get_move()
        if res is None:
            if self.score[3 - self.player] > self.score[self.player]:
                self.winner = 3 - self.player
                return self.winner
            ai = ArtificialIntelligence(self.width, self.height, self.board, 3 - self.player, self.actions + 1)
            res = ai.get_move()
            if res is None:
                if self.score[3 - self.player] == self.score[self.player]:
                    self.winner = 0
                    return self.winner
                self.winner = self.player
                return self.winner
            self.score[3 - self.player] = 150 - self.score[self.player]
            if self.score[3 - self.player] == self.score[self.player]:
                self.winner = 0
            elif self.score[3 - self.player] > self.score[self.player]:
                self.winner = 3 - self.player
            else:
                self.winner = self.player
            return self.winner
        else:
            return self.winner

    def draw_text(self, screen):
        text_color = COLOR_BLUE
        message = "Ход синего игрока"
        if self.player == 2:
            text_color = COLOR_PINK
            message = "Ход красного игрока"
        font = pygame.font.Font(None, 50)
        text_line_1 = font.render(message, True, text_color)
        text_line_2 = font.render("Осталось действий: " + str(3 - self.actions % 3), True, text_color)
        text_w = max(text_line_1.get_width(), text_line_2.get_width())
        text_h = text_line_1.get_height() + text_line_2.get_height()
        text_x = self.left + 10
        text_y = self.top - text_h - 70
        screen.blit(text_line_1, (text_x, text_y))
        screen.blit(text_line_2, (text_x, text_y + text_line_1.get_height()))
        pygame.draw.rect(screen, text_color, (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
        message = "Общая площадь колоний (S):"
        font = pygame.font.Font(None, 40)
        text_line_3 = font.render(message, True, COLOR_BLUE)
        screen.blit(text_line_3, (text_x, text_y + text_line_1.get_height() * 2 + 25))
