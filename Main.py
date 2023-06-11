import sys
import time
from Game_Board import *


def terminate():
    pygame.quit()
    sys.exit(0)


screen_width, screen_height = 850, 750
OPTIONS = ["Играть с другом", "Играть с ИИ", "Правила", "Выход"]
EXIT_BUTTON = []


def main_window(screen, x, y):
    text_color = COLOR_BLUE
    text_lines = ["Война вирусов"] + OPTIONS
    buttons = []
    width = 300
    height = 50
    current_x = x
    current_y = y
    for i in range(len(text_lines)):
        message = text_lines[i]
        font = pygame.font.Font(None, 50)
        text_line = font.render(message, True, text_color)
        if i == 0:
            pygame.draw.rect(screen, COLOR_LINES, (current_x, current_y, width, height), 0)
        pygame.draw.rect(screen, text_color, (current_x, current_y, width, height), 1)
        screen.blit(text_line, (current_x + (width - text_line.get_width()) // 2, current_y + 10))
        buttons.append([current_x, current_x + width, current_y, current_y + height])
        current_y += 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(buttons)):
                    if buttons[i][0] <= x <= buttons[i][1] and buttons[i][2] <= y <= buttons[i][3]:
                        if text_lines[i] in OPTIONS:
                            return OPTIONS.index(text_lines[i])
        pygame.display.flip()


def draw_page_number(screen, number):
    text_color = COLOR_PINK
    message1 = 'Правила игры "Война вирусов"'
    message2 = "Страница " + str(number) + " из 10"
    message3 = 'Для переключения страницы используйте клавиши "влево" и "вправо"'
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 40)
    font3 = pygame.font.Font(None, 30)
    text_line_1 = font1.render(message1, True, text_color)
    text_line_2 = font2.render(message2, True, text_color)
    text_line_3 = font3.render(message3, True, text_color)
    screen.blit(text_line_1, (55, 20))
    screen.blit(text_line_2, (55, 65))
    screen.blit(text_line_3, (55, 100))


def rules(screen):
    screen.fill(COLOR_FIELD)
    draw_page_number(screen, 1)
    draw_exit_button(screen)
    current_page = 1
    number = str(current_page // 10) + str(current_page % 10)
    file_name = "rules\\rules" + number + ".jpg"
    image = pygame.image.load(file_name)
    screen.blit(image, (40, 120))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_pushed(event.pos):
                    main_menu(screen)
            change = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_page > 1:
                        current_page -= 1
                        change = True
                if event.key == pygame.K_RIGHT:
                    if current_page < 10:
                        current_page += 1
                        change = True
            if change:
                screen.fill(COLOR_FIELD)
                draw_page_number(screen, current_page)
                draw_exit_button(screen)
                number = str(current_page // 10) + str(current_page % 10)
                file_name = "rules\\rules" + number + ".jpg"
                image = pygame.image.load(file_name)
                if current_page in [5, 6, 10]:
                    screen.blit(image, (70, 120))
                else:
                    screen.blit(image, (40, 120))
                pygame.display.update()
        pygame.display.flip()


def draw_exit_button(screen):
    text_color = COLOR_BLUE
    message = "Выход"
    font = pygame.font.Font(None, 50)
    text_line = font.render(message, True, text_color)
    text_x = 630
    text_y = 20
    text_h = text_line.get_height()
    text_w = text_line.get_width()
    screen.blit(text_line, (text_x, text_y))
    pygame.draw.rect(screen, text_color, (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
    global EXIT_BUTTON
    EXIT_BUTTON = [text_x - 10, text_x - 10 + text_w + 20, text_y - 10, text_y - 10 + text_h + 20]


def exit_button_pushed(position):
    x, y = position
    if EXIT_BUTTON[0] <= x <= EXIT_BUTTON[1] and EXIT_BUTTON[2] <= y <= EXIT_BUTTON[3]:
        return True
    return False


def main_menu(screen):
    screen.fill(COLOR_FIELD)
    user_choice = main_window(screen, 275, 50)
    if user_choice is None:
        sys.exit(0)
    elif user_choice == 0:
        # game with friend
        game(screen)
    elif user_choice == 1:
        # game with ai
        game(screen, game_with_ai=True)
    elif user_choice == 2:
        # game rules button
        rules(screen)
    else:
        # exit button
        terminate()


def draw_congratulations(screen, player):
    player_name = {1: "синий", 2: "красный"}
    player_color = {0: COLOR_LINES, 1: COLOR_BLUE, 2: COLOR_PINK}
    if player == 0:
        message = "Игра завершена! Ничья!"
    else:
        message = "Игра завершена! Победил " + player_name[player] + " игрок!"
    font = pygame.font.Font(None, 50)
    text_line = font.render(message, True, player_color[player])
    text_h = text_line.get_height()
    text_w = text_line.get_width()
    text_x = (screen_width - text_w) // 2
    text_y = 695
    screen.blit(text_line, (text_x, text_y))
    pygame.draw.rect(screen, player_color[player], (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


def draw_game_mode(screen, game_with_ai):
    text_color = COLOR_BLUE
    message = "Игра с другом"
    if game_with_ai:
        message = "Игра с ИИ: "
    font = pygame.font.Font(None, 50)
    text_line = font.render(message, True, text_color)
    text_x = 95
    text_y = 20
    text_h = text_line.get_height()
    text_w = text_line.get_width()
    if game_with_ai:
        text_line_add = font.render("ИИ - красный!", True, COLOR_PINK)
        screen.blit(text_line_add, (text_x + text_w, text_y))
        text_w += text_line_add.get_width()
    screen.blit(text_line, (text_x, text_y))
    pygame.draw.rect(screen, text_color, (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


def game(screen, game_with_ai=False):
    board = Board(15, 10)
    board.set_view(85, 225, 45)
    screen.fill(COLOR_FIELD)
    draw_exit_button(screen)
    draw_game_mode(screen, game_with_ai)
    game_is_over = False
    while True:
        if not game_is_over and game_with_ai:
            if board.player == 2:
                winner = board.get_winner()
                if winner != -1:
                    draw_congratulations(screen, winner)
                    game_is_over = True
                else:
                    time.sleep(2.5)
                    board.get_move_ai()
                screen.fill(COLOR_FIELD)
                draw_exit_button(screen)
                draw_game_mode(screen, game_with_ai)
                board.render(screen)
                pygame.display.flip()
                pygame.event.clear()
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_pushed(event.pos):
                    main_menu(screen)
                if not game_is_over:
                    board.get_click(event.pos)
        screen.fill(COLOR_FIELD)
        draw_exit_button(screen)
        draw_game_mode(screen, game_with_ai)
        board.render(screen)
        winner = board.get_winner()
        if winner != -1:
            draw_congratulations(screen, winner)
            game_is_over = True
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Война вирусов")
    icon = pygame.image.load("icon32.png")
    pygame.display.set_icon(icon)
    size = screen_width, screen_height
    main_screen = pygame.display.set_mode(size)
    main_menu(main_screen)
    pygame.quit()
