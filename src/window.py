"""
TODO:
Stop the algorithm when end point
is reached!

"""

from board import Board
from algorithms import Algorithm
import pygame
import constant as c


# Convert mouse position to cell position on screen
# We have walls at 0, 0 that aren't drawn
# So the position will start from 1, 1
def mouse_pos_to_cell(pos):
    y = x = -1
    for z in range(0, c.cell_nr + 1):
        if z * c.cell_side > pos[1] and y == -1:
            y = z
        if z * c.cell_side > pos[0] and x == -1:
            x = z
    return y, x


# Configure the board
board = Board(c.cell_nr, c.cell_nr)
board.create_dest((1, 1))
board.create_dest((c.cell_nr, c.cell_nr))
al = Algorithm(board)
end_pos = al.board.en

# Configure pygame window
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((c.cell_side * c.cell_nr, c.cell_side * c.cell_nr))
run = True

# Init the algorithm , check if it's finish
init = False
finish = False

while run:
    screen.fill(c.color['white'])
    events = pygame.event.get()
    font1 = pygame.font.SysFont("comicsansms", 50)
    # Keyboard events and closing event handling
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not init:
                ls = {al.board.st: 0}
                init = True
            if event.key == pygame.K_r and not init:
                board.create_example_board()
                end_pos = board.en
                al.reset(board)
                finish = False
            if event.key == pygame.K_BACKSPACE and not init:
                board.create_blank_board()
                end_pos = board.en
                al.reset(board)
                finish = False

    # Main logic
    if init:
        if ls != {}:
            tmp = None
            d = {}
            for k in ls.keys():
                d.update(al.run(ls[k], k))
                tmp = k
                break
            ls.pop(tmp)
            ls.update(d)
        else:
            finish = True
            init = False
        if al.end_pos_found():
            finish = True
            init = False

    # Draw the visited Nodes
    for key in al.visited_node.keys():
        rect = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
        rect.fill(c.color['rgba_red'])
        screen.blit(rect, ((key[1] - 1) * c.cell_side, (key[0] - 1) * c.cell_side))

    # Draw the finish and end nodes
    rect1 = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
    rect1.fill(c.color['yellow'])
    rect2 = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
    rect2.fill(c.color['green'])
    screen.blit(rect1, ((al.board.st[1] - 1) * c.cell_side, (al.board.st[0] - 1) * c.cell_side))
    screen.blit(rect2, ((al.board.en[1] - 1) * c.cell_side, (al.board.en[0] - 1) * c.cell_side))

    # Assign cells to walls with mouse press
    if pygame.mouse.get_pressed()[0]:
        al.board.create_one_wall(mouse_pos_to_cell(pygame.mouse.get_pos()))

    # Draw the board
    for i in range(c.cell_nr):
        pygame.draw.line(screen, c.color['black'], (0, i * c.cell_side),
                         (c.cell_nr * c.cell_side, i * c.cell_side))
        for j in range(c.cell_nr):
            pygame.draw.line(screen, c.color['black'], (j * c.cell_side, 0),
                             (j * c.cell_side, c.cell_side * c.cell_nr))
            # Draw the walls ?
            if al.board.matrix[i + 1][j + 1] == -1:
                rect = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
                rect.fill(c.color['rgba_blue'])
                screen.blit(rect, (j * c.cell_side, i * c.cell_side))

    # Draw the shortest path if the algorithm is finished
    # and the end position is found
    if finish and al.end_pos_found():
        if end_pos != al.board.st:
            al.find_path(end_pos)
            end_pos = al.path[-1]
        for i in al.path:
            rect = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
            rect.fill(c.color['black'])
            screen.blit(rect, ((i[1] - 1) * c.cell_side, (i[0] - 1) * c.cell_side))

    pygame.display.update()
    clock.tick(60)
