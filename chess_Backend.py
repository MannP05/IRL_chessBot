import pygame
import json

class Chessboard:
    def __init__(self, board_file, cell_size=80):
        self.board_array = self.load_board(board_file)
        self.cell_size = cell_size
        self.width = len(self.board_array[0]) * cell_size
        self.height = len(self.board_array) * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chessboard")

    def load_board(self, board_file):
        with open(board_file, 'r') as f:
            board_array = json.load(f)
        return board_array

    def draw_board(self):
        colors = [(255, 255, 255), (0, 0, 0)]  # White and Black
        for i in range(len(self.board_array)):
            for j in range(len(self.board_array[i])):
                color = colors[self.board_array[i][j]]
                pygame.draw.rect(self.screen, color, pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()
        pygame.quit()

# Initialize Pygame and create the chessboard
pygame.init()
chessboard = Chessboard('chessboard_array.json')
chessboard.update()
