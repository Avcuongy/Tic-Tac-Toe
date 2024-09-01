import tkinter as tk
from tkinter import PhotoImage
import pygame as py

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='lightblue')

        py.init()
        py.mixer.init()
        self.music_file = 'Audio And Picture/BGM.mp3'
        self.image_file = 'Audio And Picture/Hello.png'
        self.frames = {'menu': None, 'game': None, 'result': None}
        
        self.LoadAssets()
        self.CreateMenu()

    def LoadAssets(self):
        self.menu_image = PhotoImage(file=self.image_file)
        self.PlayMusic()

    def PlayMusic(self):
        py.mixer.music.load(self.music_file)
        py.mixer.music.set_volume(0.2)
        py.mixer.music.play(-1)

    def StopMusic(self):
        py.mixer.music.stop()

    def CreateCloseButton(self, frame):
        close_button = tk.Button(frame, text='X', font=('Roboto', 15, 'bold'), command=self.ExitProgram, bg='red', fg='white', width=3, height=1)
        close_button.place(relx=0.99, rely=0.01, anchor='ne')

    def CreateMenu(self):
        self.ClearScreen()
        self.frames['menu'] = tk.Frame(self.root, bg='lightblue')
        self.frames['menu'].pack(expand=True, fill='both')
        
        self.CreateCloseButton(self.frames['menu'])

        container = tk.Frame(self.frames['menu'], bg='lightblue')
        container.place(relx=0.5, rely=0.5, anchor='center')

        image_label = tk.Label(container, image=self.menu_image, bg='lightblue')
        image_label.grid(row=0, column=0, padx=(0, 20), pady=20)

        menu_content_frame = tk.Frame(container, bg='lightblue')
        menu_content_frame.grid(row=0, column=1, pady=20)

        tk.Label(menu_content_frame, text="Trò chơi Tic Tac Toe", font=('Roboto', 36, 'bold'), bg='lightblue').pack(pady=(0, 30))
        tk.Button(menu_content_frame, text="Start", font=('Roboto', 24), command=self.StartGame, width=15, bg='white', fg='black').pack(pady=10)
        tk.Button(menu_content_frame, text="Exit", font=('Roboto', 24), command=self.ExitProgram, width=15, bg='white', fg='black').pack(pady=10)

    def StartGame(self):
        self.ClearScreen()
        self.CreateGame()

    def CreateGame(self):
        self.frames['game'] = tk.Frame(self.root, bg='lightblue')
        self.frames['game'].pack(expand=True, fill='both')

        self.CreateCloseButton(self.frames['game'])

        self.turn = 'X'
        self.buttons = [[None] * 3 for _ in range(3)]
        self.CreateWidgets()

    def CreateWidgets(self):
        game_board = tk.Frame(self.frames['game'], bg='lightblue')
        game_board.place(relx=0.5, rely=0.5, anchor='center')

        for r in range(3):
            for c in range(3):
                btn = tk.Button(game_board, text=' ', font=('Roboto', 40), width=5, height=2,
                                command=lambda r=r, c=c: self.OnButtonClick(r, c),
                                bg='white', fg='black', relief=tk.SOLID, borderwidth=2)
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

    def OnButtonClick(self, r, c):
        """Handle button click during the game."""
        if self.buttons[r][c]['text'] == ' ' and self.turn == 'X':
            self.buttons[r][c]['text'] = 'X'
            self.buttons[r][c]['fg'] = 'black'
            if self.CheckWinner('X'):
                self.EndGame("WINNERRRRRR")
                return
            if self.IsBoardFull():
                self.EndGame("DRAW")
                return
            self.turn = 'O'
            self.root.after(500, self.AiMove)

    def AiMove(self):
        best_move, _ = self.Minimax(-float('inf'), float('inf'), True)
        if best_move:
            r, c = best_move
            self.buttons[r][c]['text'] = 'O'
            self.buttons[r][c]['fg'] = 'black'
            if self.CheckWinner('O'):
                self.EndGame("Ngu Zữ Trừi")
                return
            if self.IsBoardFull():
                self.EndGame("DRAW")
                return
        self.turn = 'X'

    def Minimax(self, alpha, beta, is_maximizing):
        winner = self.CheckWinner('O') or self.CheckWinner('X')
        if winner:
            return None, 1 if winner == 'O' else -1
        if self.IsBoardFull():
            return None, 0

        best_move, best_score = None, -float('inf') if is_maximizing else float('inf')

        for r in range(3):
            for c in range(3):
                if self.buttons[r][c]['text'] == ' ':
                    self.buttons[r][c]['text'] = 'O' if is_maximizing else 'X'
                    _, score = self.Minimax(alpha, beta, not is_maximizing)
                    self.buttons[r][c]['text'] = ' '
                    if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
                        best_score, best_move = score, (r, c)
                    if is_maximizing:
                        alpha = max(alpha, best_score)
                    else:
                        beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_move, best_score

    def CheckWinner(self, player):
        b = self.buttons
        lines = [
            [b[i][0]['text'] == player and b[i][1]['text'] == player and b[i][2]['text'] == player for i in range(3)],
            [b[0][i]['text'] == player and b[1][i]['text'] == player and b[2][i]['text'] == player for i in range(3)],
            [b[0][0]['text'] == player and b[1][1]['text'] == player and b[2][2]['text'] == player],
            [b[0][2]['text'] == player and b[1][1]['text'] == player and b[2][0]['text'] == player]
        ]
        return player if any(any(line) for line in lines) else None

    def IsBoardFull(self):
        return all(self.buttons[r][c]['text'] != ' ' for r in range(3) for c in range(3))

    def EndGame(self, message):
        self.ClearScreen()
        self.frames['result'] = tk.Frame(self.root, bg='lightblue')
        self.frames['result'].pack(expand=True, fill='both')

        self.CreateCloseButton(self.frames['result'])

        result_box = tk.Frame(self.frames['result'], bg='white', padx=50, pady=50, relief=tk.SOLID, borderwidth=2)
        result_box.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(result_box, text=message, font=('Roboto', 30, 'bold'), bg='white', fg='black').pack(pady=20)
        tk.Button(result_box, text="Play Again", font=('Roboto', 20), command=self.StartGame, width=15, bg='green', fg='white').pack(pady=10)
        tk.Button(result_box, text="Back To Menu", font=('Roboto', 20), command=self.CreateMenu, width=15, bg='blue', fg='white').pack(pady=10)

    def ClearScreen(self):
        for frame in self.frames.values():
            if frame:
                frame.destroy()

    def ExitProgram(self):
        self.StopMusic()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
