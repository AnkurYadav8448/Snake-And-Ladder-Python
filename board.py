
# ---------------- BOARD CONFIGURATION ----------------

CELL_SIZE = 58
BOARD_START = 20

SNAKES = {
    99: 54,
    70: 55,
    52: 29,
    25: 2
}

LADDERS = {
    4: 25,
    13: 46,
    42: 63,
    50: 69
}


# ---------------- GET POSITION ----------------

def get_position(number):

    row = (number - 1) // 10
    col = (number - 1) % 10

    if row % 2 == 1:
        col = 9 - col

    x = BOARD_START + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_START + (9 - row) * CELL_SIZE + CELL_SIZE // 2

    return x, y


# ---------------- DRAW BOARD ----------------

def draw_board(canvas):

    canvas.delete("all")

    # Draw all 100 cells
    for number in range(1, 101):

        x, y = get_position(number)

        x1 = x - CELL_SIZE // 2
        y1 = y - CELL_SIZE // 2
        x2 = x + CELL_SIZE // 2
        y2 = y + CELL_SIZE // 2

        row = (number - 1) // 10
        col = (number - 1) % 10

        if row % 2 == 1:
            col = 9 - col

        color = "#FDE68A" if (row + col) % 2 == 0 else "#BFDBFE"

        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="black",
            width=1
        )

    # Draw snakes
    for start, end in SNAKES.items():

        x1, y1 = get_position(start)
        x2, y2 = get_position(end)

        canvas.create_line(
            x1, y1,
            x1 + 30, (y1 + y2) / 2,
            x2, y2,
            fill="red",
            width=7,
            smooth=True
        )

        canvas.create_oval(
            x1 - 8, y1 - 8,
            x1 + 8, y1 + 8,
            fill="red",
            outline="black"
        )

    # Draw ladders
    for start, end in LADDERS.items():

        x1, y1 = get_position(start)
        x2, y2 = get_position(end)

        canvas.create_line(
            x1 - 8, y1,
            x2 - 8, y2,
            fill="green",
            width=4
        )

        canvas.create_line(
            x1 + 8, y1,
            x2 + 8, y2,
            fill="green",
            width=4
        )

        for i in range(1, 5):

            x = x1 + (x2 - x1) * i / 5
            y = y1 + (y2 - y1) * i / 5

            canvas.create_line(
                x - 8, y,
                x + 8, y,
                fill="brown",
                width=3
            )

    # Draw numbers last
    for number in range(1, 101):

        x, y = get_position(number)

        canvas.create_text(
            x, y,
            text=str(number),
            font=("Arial", 12, "bold"),
            fill="black"
        )
