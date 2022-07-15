import pygame as py
import engine

width = height = 512
dimension = 8
sq_size = height//dimension
max_fps = 15
images = {}

def load_images():
    pieces = ["wR","wN","wB","wQ","wK","wP","bR","bN","bB","bQ","bK","bP"]
    for piece in pieces:
        images[piece] = py.transform.scale(py.image.load("images/"+ piece + ".png"), (sq_size, sq_size))

def main():
    py.init()
    clock = py.time.Clock()
    win = py.display.set_mode((width, height))
    win.fill(py.Color("white"))
    gs = engine.gameState()
    load_images()
    running = True
    sqSelected = ()
    player_clicks = []

    while running:

        for e in py.event.get():

            if e.type == py.QUIT:
                running = False

            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                col = location[0]//sq_size
                row = location[1]//sq_size
                
                if sqSelected == (row, col):
                    sqSelected = ()
                    player_clicks = []

                else:
                    sqSelected = (row, col)
                    player_clicks.append(sqSelected)

                if len(player_clicks) == 2:
                    move = engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())                    
                    gs.make_move(move)
                    print(sqSelected)
                    sqSelected = ()
                    player_clicks = []
                
            elif e.type == py.KEYDOWN:
                if e.key == py.K_z:
                    gs.undo_move()

        drawGameState(win, gs, sqSelected)
        clock.tick(max_fps)
        py.display.flip()

def drawGameState(win, gs, sqSelected):
    drawBoard(win, sqSelected, gs)
    drawPieces(win, gs.board)

def drawBoard(win, sqSelected, gs):
    colours = [py.Color("white"), py.Color(180,140,90)]
    for r in range(dimension):
        for c in range(dimension):
            if sqSelected == (r,c):
                colour = py.Color("yellow")
            else:
                colour = colours[((r+c) % 2)]
            py.draw.rect(win, colour, py.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def drawPieces(win, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                win.blit(images[piece], py.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

if __name__ == "__main__":
    main()