# Snake and Ladder Game - Python + Tkinter
import tkinter as tk
import random

# ---------- game settings ----------
snakes = {99: 54, 70: 55, 52: 29, 36: 6}      # head: tail
ladders = {4: 25, 13: 46, 42: 63, 50: 69}     # bottom: top

player_names = ["Player 1", "Player 2"]
player_colors = ["red", "blue"]

# animation speed (milliseconds)
dice_speed = 70
step_speed = 220
pause_speed = 500
dice_frames = 14

# dice dots: (column, row) in a 3x3 grid
dice_dots = {
    1: [(1, 1)],
    2: [(0, 0), (2, 2)],
    3: [(0, 0), (1, 1), (2, 2)],
    4: [(0, 0), (2, 0), (0, 2), (2, 2)],
    5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
    6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)],
}

# ---------- game variables ----------
positions = [0, 0]       # 0 means START
current_player = 0       # 0 = Player 1, 1 = Player 2
is_busy = False          # True while dice or token is animating
game_over = False
last_dice = 0

# ---------- check snakes and ladders ----------
all_starts = list(snakes.keys()) + list(ladders.keys())
if len(all_starts) != len(set(all_starts)):
    print("Error: a snake and a ladder start on the same square")
for end in list(snakes.values()) + list(ladders.values()):
    if end in all_starts:
        print("Error: square", end, "is the end of one and the start of another")

# ---------- window and board size ----------
root = tk.Tk()
root.title("Snake and Ladder")
root.configure(bg="#0B1F4B")
root.resizable(False, False)

# smaller board on small screens, so the buttons are never cut off
cell = (root.winfo_screenheight() - 230) // 10
if cell > 54:
    cell = 54
if cell < 36:
    cell = 36
left = 12
top = 12
start_area = 40
board_width = 10 * cell + 2 * left
board_height = 10 * cell + top + start_area


# ---------- board coordinates ----------
def get_row_col(square):
    # row 0 is the bottom row, column 0 is the left column
    row = (square - 1) // 10
    col = (square - 1) % 10
    if row % 2 == 1:          # odd rows go right to left
        col = 9 - col
    return row, col


def get_position(square):
    # the only place where x, y is calculated (used for squares AND tokens)
    if square == 0:
        x = left + cell / 2
        y = top + 10 * cell + start_area / 2
        return x, y
    row, col = get_row_col(square)
    x = left + col * cell + cell / 2
    y = top + (9 - row) * cell + cell / 2
    return x, y


# ---------- drawing ----------
def draw_board():
    canvas.delete("all")
    font_size = max(8, cell // 5)
    for square in range(1, 101):
        x, y = get_position(square)
        row, col = get_row_col(square)
        if (row + col) % 2 == 0:
            color = "#FFE066"
        else:
            color = "#A5D8FF"
        canvas.create_rectangle(x - cell / 2, y - cell / 2,
                                x + cell / 2, y + cell / 2,
                                fill=color, outline="#334155")
        canvas.create_text(x - cell / 2 + 4, y - cell / 2 + 3,
                           text=str(square), anchor="nw",
                           font=("Arial", font_size, "bold"))

    x, y = get_position(0)
    canvas.create_text(x + cell * 0.45, y, text="START", anchor="w",
                       fill="#FFD60A", font=("Arial", 12, "bold"))

    for bottom in ladders:
        draw_ladder(bottom, ladders[bottom])
    for head in snakes:
        draw_snake(head, snakes[head])


def draw_ladder(bottom, top_square):
    x1, y1 = get_position(bottom)
    x2, y2 = get_position(top_square)
    dx = x2 - x1
    dy = y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    # small sideways step, used to draw the two rails
    sx = -dy / length * cell * 0.14
    sy = dx / length * cell * 0.14

    canvas.create_line(x1 + sx, y1 + sy, x2 + sx, y2 + sy,
                       fill="#2E9E4F", width=4)
    canvas.create_line(x1 - sx, y1 - sy, x2 - sx, y2 - sy,
                       fill="#2E9E4F", width=4)

    rungs = int(length // (cell * 0.45))
    if rungs < 3:
        rungs = 3
    for i in range(1, rungs):
        cx = x1 + dx * i / rungs
        cy = y1 + dy * i / rungs
        canvas.create_line(cx + sx, cy + sy, cx - sx, cy - sy,
                           fill="#1E7B3A", width=3)


def draw_snake(head, tail):
    x1, y1 = get_position(head)
    x2, y2 = get_position(tail)
    dx = x2 - x1
    dy = y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    px = -dy / length          # sideways direction
    py = dx / length
    sx = px * cell * 0.18
    sy = py * cell * 0.18

    # wavy body: points on the line moved left/right one after another
    waves = [0, 1, -1, 1, -1, 1, 0]
    points = []
    for i in range(len(waves)):
        t = i / (len(waves) - 1)
        points.append(x1 + dx * t + sx * waves[i])
        points.append(y1 + dy * t + sy * waves[i])
    canvas.create_line(points, fill="#D62828", width=max(4, cell // 9),
                       smooth=True, capstyle="round")

    r = cell * 0.17
    canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r,
                       fill="#8B1A1A", outline="#D62828")
    eye = r * 0.35
    for side in (1, -1):
        ex = x1 + px * r * 0.45 * side
        ey = y1 + py * r * 0.45 * side
        canvas.create_oval(ex - eye, ey - eye, ex + eye, ey + eye,
                           fill="white", outline="")
    tip = cell * 0.06
    canvas.create_oval(x2 - tip, y2 - tip, x2 + tip, y2 + tip,
                       fill="#D62828", outline="")


def draw_tokens():
    canvas.delete("token")
    r = cell * 0.19
    shift = cell * 0.22      # keeps both tokens visible on the same square
    for player in range(2):
        x, y = get_position(positions[player])
        if player == 0:
            x = x - shift
        else:
            x = x + shift
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           fill=player_colors[player], outline="white",
                           width=2, tags="token")
        canvas.create_text(x, y, text=str(player + 1), fill="white",
                           font=("Arial", max(8, int(r)), "bold"),
                           tags="token")
    canvas.tag_raise("winner")


def draw_dice(value):
    # value 0 means no roll yet, so draw a "?"
    dice_canvas.delete("all")
    dice_canvas.create_rectangle(8, 8, 102, 102, fill="white",
                                 outline="#999999", width=3)
    if value == 0:
        dice_canvas.create_text(55, 55, text="?", fill="#999999",
                                font=("Arial", 36, "bold"))
        return
    spots = [25, 55, 85]
    for col, row in dice_dots[value]:
        x = spots[col]
        y = spots[row]
        dice_canvas.create_oval(x - 9, y - 9, x + 9, y + 9, fill="black")


def show_winner(player):
    x = board_width / 2
    y = top + 5 * cell
    canvas.create_rectangle(x - 190, y - 60, x + 190, y + 60,
                            fill="#0B1F4B", outline="#FFD60A", width=4,
                            tags="winner")
    canvas.create_text(x, y - 20, text=player_names[player].upper() + " WINS!",
                       fill="#FFD60A", font=("Arial", 28, "bold"),
                       tags="winner")
    canvas.create_text(x, y + 25, text="*** Congratulations! ***",
                       fill="white", font=("Arial", 16, "bold"),
                       tags="winner")


# ---------- labels and buttons ----------
def position_text(player):
    if positions[player] == 0:
        return "START"
    return str(positions[player])


def update_labels():
    p1_label.config(text="Player 1 Position: " + position_text(0))
    p2_label.config(text="Player 2 Position: " + position_text(1))
    if game_over:
        turn_label.config(text="Current Turn: Game Over")
    else:
        turn_label.config(text="Current Turn: " + player_names[current_player])
    if last_dice == 0:
        dice_label.config(text="Last Dice Result: -")
    else:
        dice_label.config(text="Last Dice Result: " + str(last_dice))


def set_status(message):
    status_label.config(text="Status: " + message)


def set_buttons(state):
    # state is "normal" or "disabled"
    roll_button.config(state=state)
    restart_button.config(state=state)


# ---------- game logic ----------
def roll_dice():
    global is_busy
    if is_busy or game_over:      # stops double clicks
        return
    is_busy = True
    set_buttons("disabled")
    player = current_player       # remember who is playing this turn
    set_status(player_names[player] + " is rolling the dice...")
    animate_dice(player, 0)


def animate_dice(player, count):
    global last_dice
    if count < dice_frames:
        draw_dice(random.randint(1, 6))
        root.after(dice_speed, animate_dice, player, count + 1)
    else:
        last_dice = random.randint(1, 6)     # final dice result
        draw_dice(last_dice)
        update_labels()
        set_status(player_names[player] + " rolled a " + str(last_dice) + ".")
        root.after(pause_speed, start_move, player, last_dice)


def start_move(player, dice):
    target = positions[player] + dice
    if target > 100:
        set_status(player_names[player] + " needs an exact roll to reach 100. Turn skipped.")
        root.after(900, end_turn, player)
    else:
        move_token(player, target, check_square)


def move_token(player, target, next_step):
    # moves one square at a time, then calls next_step(player)
    if positions[player] == target:
        root.after(step_speed, next_step, player)
        return
    if positions[player] < target:
        positions[player] = positions[player] + 1
    else:
        positions[player] = positions[player] - 1
    draw_tokens()
    update_labels()
    root.after(step_speed, move_token, player, target, next_step)


def check_square(player):
    square = positions[player]
    if square == 100:
        winner(player)
    elif square in ladders:
        set_status(player_names[player] + " found a ladder! " + str(square) + " -> " + str(ladders[square]))
        root.after(pause_speed, move_token, player, ladders[square], after_slide)
    elif square in snakes:
        set_status(player_names[player] + " was bitten by a snake! " + str(square) + " -> " + str(snakes[square]))
        root.after(pause_speed, move_token, player, snakes[square], after_slide)
    else:
        end_turn(player)


def after_slide(player):
    # no second snake/ladder check here, so a slide never triggers another one
    if positions[player] == 100:
        winner(player)
    else:
        end_turn(player)


def end_turn(player):
    # the ONLY place where the turn is switched
    global current_player, is_busy
    current_player = 1 - player
    is_busy = False
    set_buttons("normal")
    update_labels()
    set_status(player_names[current_player] + "'s turn. Click ROLL DICE.")


def winner(player):
    global game_over, is_busy
    game_over = True
    is_busy = False
    roll_button.config(state="disabled")
    restart_button.config(state="normal")
    update_labels()
    set_status(player_names[player] + " reached 100 and wins! Click RESTART GAME to play again.")
    show_winner(player)


def restart_game():
    global positions, current_player, is_busy, game_over, last_dice
    if is_busy:
        return
    positions = [0, 0]
    current_player = 0
    is_busy = False
    game_over = False
    last_dice = 0
    canvas.delete("winner")
    draw_dice(0)
    draw_tokens()
    update_labels()
    set_buttons("normal")
    set_status("New game! Player 1 starts. Click ROLL DICE!")


# ---------- screen layout ----------
title = tk.Label(root, text="SNAKE AND LADDER", font=("Arial", 28, "bold"),
                 fg="#FFD60A", bg="#0B1F4B")
title.grid(row=0, column=0, columnspan=2, pady=(8, 4))

canvas = tk.Canvas(root, width=board_width, height=board_height,
                   bg="#0B1F4B", highlightthickness=0)
canvas.grid(row=1, column=0, padx=(12, 6), pady=(0, 10))

panel = tk.Frame(root, bg="#12306B", width=310)
panel.grid(row=1, column=1, padx=(6, 12), pady=(0, 10), sticky="ns")

tk.Label(panel, text="DICE", font=("Arial", 14, "bold"),
         fg="white", bg="#12306B").pack(pady=(12, 4))
dice_canvas = tk.Canvas(panel, width=110, height=110, bg="#12306B",
                        highlightthickness=0)
dice_canvas.pack()

dice_label = tk.Label(panel, font=("Arial", 13, "bold"), fg="white",
                      bg="#12306B")
dice_label.pack(pady=(6, 10))

p1_label = tk.Label(panel, font=("Arial", 13, "bold"), fg="#FF8A8A",
                    bg="#12306B")
p1_label.pack(padx=14, anchor="w")
p2_label = tk.Label(panel, font=("Arial", 13, "bold"), fg="#8DB8FF",
                    bg="#12306B")
p2_label.pack(padx=14, anchor="w")
turn_label = tk.Label(panel, font=("Arial", 13, "bold"), fg="#FFD60A",
                      bg="#12306B")
turn_label.pack(padx=14, pady=(6, 0), anchor="w")

status_label = tk.Label(panel, font=("Arial", 12), fg="white", bg="#12306B",
                        wraplength=270, justify="left", height=4,
                        anchor="nw")
status_label.pack(padx=14, pady=(8, 8), anchor="w")

roll_button = tk.Button(panel, text="ROLL DICE", font=("Arial", 16, "bold"),
                        bg="#2EB84B", fg="white", activebackground="#249A3D",
                        activeforeground="white",
                        disabledforeground="#CFE8D5",
                        width=16, height=2, command=roll_dice)
roll_button.pack(pady=(0, 8))

restart_button = tk.Button(panel, text="RESTART GAME",
                           font=("Arial", 16, "bold"), bg="#FF8C1A",
                           fg="white", activebackground="#D97706",
                           activeforeground="white",
                           disabledforeground="#F5DDBF",
                           width=16, height=2, command=restart_game)
restart_button.pack(pady=(0, 14))

# ---------- start ----------
draw_board()
draw_dice(0)
draw_tokens()
update_labels()
set_status("Player 1 starts. Click ROLL DICE!")

# put the window in the middle of the screen
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2 - 20
if y < 0:
    y = 0
root.geometry("+" + str(x) + "+" + str(y))

root.mainloop()
