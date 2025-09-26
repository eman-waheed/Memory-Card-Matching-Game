import tkinter as tk
import random
import time

class MemoryCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Matching Game")

        # Variables
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.start_time = None
        self.timer_running = False
        self.card_values = []
        self.flipped = []

        # Labels
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        self.moves_label = tk.Label(self.info_frame, text="Moves: 0", font=("Arial", 12))
        self.moves_label.grid(row=0, column=0, padx=20)

        self.timer_label = tk.Label(self.info_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.grid(row=0, column=1, padx=20)

        # Restart Button
        self.restart_btn = tk.Button(self.info_frame, text="Restart", command=self.restart_game, font=("Arial", 12))
        self.restart_btn.grid(row=0, column=2, padx=20)

        # Board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.create_board()
        self.update_timer()

    def create_board(self):
        self.card_values = list(range(1, 9)) * 2  # 8 pairs for 4x4 grid
        random.shuffle(self.card_values)
        self.flipped = [False] * len(self.card_values)

        # Create buttons
        for i in range(4):
            row = []
            for j in range(4):
                idx = i * 4 + j
                btn = tk.Button(self.board_frame, text="*", width=6, height=3,
                                command=lambda idx=idx: self.flip_card(idx))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        self.start_time = time.time()
        self.timer_running = True

    def flip_card(self, idx):
        if self.flipped[idx] or self.second_card is not None:
            return

        i, j = divmod(idx, 4)
        self.buttons[i][j].config(text=str(self.card_values[idx]))
        self.flipped[idx] = True

        if self.first_card is None:
            self.first_card = idx
        else:
            self.second_card = idx
            self.root.after(1000, self.check_match)

        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")

    def check_match(self):
        if self.card_values[self.first_card] != self.card_values[self.second_card]:
            for idx in [self.first_card, self.second_card]:
                i, j = divmod(idx, 4)
                self.buttons[i][j].config(text="*")
                self.flipped[idx] = False

        self.first_card = None
        self.second_card = None

        if all(self.flipped):
            self.timer_running = False
            tk.messagebox.showinfo("Congratulations!", f"You won in {self.moves} moves and {int(time.time()-self.start_time)} seconds!")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    def restart_game(self):
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 0s")
        self.create_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryCardGame(root)
    root.mainloop()
