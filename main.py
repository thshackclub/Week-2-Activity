import random
import curses

# Define the screen
s = curses.initscr()

# Set the cursor to 0 so it's invisible
curses.curs_set(0)

# Get the width and the height
sh, sw, = s.getmaxyx()

# Create a new window from the height and width at the top left corner
w = curses.newwin(sh, sw, 0, 0)

# Enable all keys
w.keypad(1)

# Determine how fast the snake moves
w.timeout(100)

# The snake's initial X position
snk_x = sw/4

# The snake's initial Y position
snk_y = sh/2

# Create the initial snake body parts
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# Set the first food item at the center of the screen
food = [sh/2, sw/2]

# Add the food to the screen
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
# Init direction of the snake
key = curses.KEY_RIGHT

while True:
    next_key =  w.getch()
    
    wrong_operation = True if (next_key==-1 or next_key==curses.KEY_DOWN and key == curses.KEY_UP\
                            or key==curses.KEY_DOWN and next_key == curses.KEY_UP \
                            or next_key==curses.KEY_LEFT and key == curses.KEY_RIGHT\
                            or key==curses.KEY_LEFT and next_key == curses.KEY_RIGHT) else False  
    if wrong_operation:
        key = key
    else:
        key = next_key

    if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:

        curses.nocbreak()
        s.keypad(False)
        curses.echo()
        curses.endwin()
        print("Oops, you lost!")
        break
        quit()

    
    
    new_head = [snake[0][0], snake[0][1]]

    # Player presses key down
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    # Player presses key up
    if key == curses.KEY_UP:
        new_head[0] -= 1
    # Player presses key left
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    # Player presses key right
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert the new head of the snake
    snake.insert(0, new_head)

    # Check if the snake ran into the food
    if snake[0] == food:
        # Since the snake ate the food, we need to set a new food position
        food = None
        while food is None:
            # Randomize the position of the new food
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            # Set the new food is the new food is not in the snake
            food = nf if nf not in snake else None
        # Add the new food position to the screen
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        # Handle snake not running into the food
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    try:
        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
    except:
        print("Oops, you lost!")