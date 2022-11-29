import numpy as np
import pygame
import sys
import math
from scipy.signal import convolve2d

GREEN = (0,200,0)
BLACK = (0,0,0)
RED = (200,0,0)
BLUE = (0,0,200)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)

#creates game board matrix
def createBoard():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

#changes value of required slot
def dropPiece(board, row, col, piece):
	board[row][col] = piece

#checks if column is full
def isValid(board, col):
	return board[ROW_COUNT-1][col] == 0

#checks if row is open
def getOpenRow(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

#prints board to screen
def printBoard(board):
	print(np.flip(board, 0))

#checks if player's piece are connect in a row of 4
def winCon(board, player):
    horizontal_kernel = np.array([[ 1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

    for kernel in detection_kernels:
        if (convolve2d(board == player, kernel, mode="valid") == 4).any():
            return True
    return False

#creates a GUI for drawing the board
def drawBoard(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, GREEN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def main():
    pygame.init()
    pygame.display.update()
    myfont = pygame.font.SysFont("ariel", 80)
    board = createBoard()
    drawBoard(board)
    printBoard(board)
    gameOver = False
    turn = 0

    while not gameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if isValid(board, col):
                        row = getOpenRow(board, col)
                        dropPiece(board, row, col, 1)

                        if winCon(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            gameOver = True

                #Player 2 Input
                else:				
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if isValid(board, col):
                        row = getOpenRow(board, col)
                        dropPiece(board, row, col, 2)

                        if winCon(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            gameOver = True

                printBoard(board)
                drawBoard(board)

                turn += 1
                turn = turn % 2

                if gameOver:
                    pygame.time.wait(2000)

if __name__ == '__main__':
    main()
