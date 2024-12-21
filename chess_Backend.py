import pygame
import numpy as np
from sample import ChessboardDetector  # Make sure 'sample.py' is in the same directory

class ChessboardSimulation:
    def __init__(self, board_size, cell_size=100):
        pygame.init()
        self.board_size = board_size
        self.cell_size = cell_size
        self.width = board_size[0] * cell_size
        self.height = board_size[1] * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chessboard Simulation")
        self.clock = pygame.time.Clock()
        self.detector = ChessboardDetector(board_size)

    def draw_board(self, board_array):
        colors = [(255, 255, 255), (0, 0, 0)]  # White and Black
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                color = colors[board_array[i][j]]
                pygame.draw.rect(self.screen, color, pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
    
    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            board_array = self.detector.get_chessboard_array()
            if board_array is not None:
                self.screen.fill((0, 0, 0))
                self.draw_board(board_array)
                pygame.display.flip()
            
            self.clock.tick(30)  # Limit to 30 FPS

        self.detector.release_camera()
        pygame.quit()

if __name__ == "__main__":
    simulation = ChessboardSimulation((3, 3))
    simulation.update()
