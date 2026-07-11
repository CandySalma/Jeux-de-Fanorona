import tkinter as tk
from tkinter import messagebox

class Game5x5:
    def __init__(self, master, player1_name, player2_name, player1_color, player2_color, num_rounds, menu_frame, game_frame):
        self.master = master
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.num_rounds = num_rounds
        self.current_round = 1
        self.scores = {player1_name: 0, player2_name: 0}
        
        self.menu_frame = menu_frame
        self.game_frame = game_frame
        
        self.master.title("Fanorona 5x5")
        
        self.canvas = tk.Canvas(game_frame, width=500, height=500, bg="white")
        self.canvas.pack(pady=20)
        
        self.score_frame = tk.Frame(game_frame)
        self.score_frame.pack(pady=20)
        
        self.setup_scoreboard()
        self.setup_board()
        self.setup_menu()
        
        self.positions = {
            player1_name: [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
            player2_name: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        }
        self.original_positions = {k: list(v) for k, v in self.positions.items()}
        
        self.moves_count = {player1_name: {pos: 0 for pos in self.positions[player1_name]},
                            player2_name: {pos: 0 for pos in self.positions[player2_name]}}

        self.turn = player1_name
        self.selected_boule = None
        self.draw_boules()
        self.draw_highlight()
        
        self.canvas.bind("<Button-1>", self.click_handler)
    
    def setup_scoreboard(self):
        # Configure the scoreboard display
        tk.Label(self.score_frame, text=f"{self.player1_name} ({self.player1_color})", font=("Helvetica", 16)).pack(side=tk.LEFT)
        tk.Label(self.score_frame, text="VS", font=("Helvetica", 16)).pack(side=tk.LEFT)
        tk.Label(self.score_frame, text=f"{self.player2_name} ({self.player2_color})", font=("Helvetica", 16)).pack(side=tk.LEFT)
    
    def setup_board(self):
        # Draw the game board
        for row in range(5):
            for col in range(5):
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
    
    def setup_menu(self):
        # Optionally setup menu for in-game options
        pass
    
    def draw_boules(self):
        # Draw the boules on the board
        for player, positions in self.positions.items():
            color = self.player1_color if player == self.player1_name else self.player2_color
            for (row, col) in positions:
                self.draw_boule(row, col, color)
    
    def draw_boule(self, row, col, color):
        x = col * 100 + 50
        y = row * 100 + 50
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black")
    
    def draw_highlight(self):
        # Highlight selected boule or current turn
        pass
    
    def click_handler(self, event):
        # Handle click events on the canvas
        pass
