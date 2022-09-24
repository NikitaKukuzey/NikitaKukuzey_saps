import tkinter
import random


def check_coord():
    global s
    coords = random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step
    while coords in s:
        coords = random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step
    s.append(coords)
    return coords


def always_right():
    return (step, 0)


def always_left():
    return (-step, 0)


def always_up():
    return (0, step)


def always_down():
    return (0, -step)


def random_move():
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])


def go_to_player(x):
    global xm
    global ym
    cord = canvas.coords(player)
    if cord[0] - x[0] != 0:
        if cord[0] - x[0] > 0:
            xm = step
        else:
            xm = -step
    if cord[1] - x[1] != 0:
        if cord[1] - x[1] > 0:
            ym = step
        else:
            ym = -step
    else:
        check_move()
    return xm, ym


def prepare_and_start():
    global player, exit, fires, enemies, k, s
    s = []
    canvas.delete("all")
    player_pos = check_coord()
    player = canvas.create_image(player_pos, image=player_pic, anchor='nw')
    exit_pos = check_coord()
    exit = canvas.create_image(exit_pos, image=exit_pic, anchor='nw')
    N_FIRES = 6  # Число клеток, заполненных огнем
    fires = []
    for i in range(N_FIRES):
        fire_pos = check_coord()
        fire = canvas.create_image(fire_pos, image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 6  # Число врагов
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = check_coord()
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append(
            (enemy, random.choice([always_up, always_down, always_left, random_move, always_right, go_to_player])))
    label.config(text="Найди выход!")
    k = 3
    master.bind("<KeyPress>", key_pressed)


def do_nothing(x):
    pass


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(player)[1] == 660:
        canvas.move(player, 0, -660)
    if canvas.coords(player)[1] == -60:
        canvas.move(player, 0, +660)
    if canvas.coords(player)[0] == 660:
        canvas.move(player, -660, 0)
    if canvas.coords(player)[0] == -60:
        canvas.move(player, +660, 0)


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]) != canvas.coords(exit):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    global k
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(player, (0, +step))
    if event.keysym == 'Left':
        move_wrap(player, (-step, 0))
    if event.keysym == 'Right':
        move_wrap(player, (+step, 0))
    if event.keysym == '1':
        if k == 3:
            k = 0
    if k > 2:
        for enemy in enemies:
            coord = canvas.coords(enemy[0])
            if enemy[1] == go_to_player:
                direction = go_to_player(coord)
            else:
                direction = enemy[1]()  # вызвать функцию перемещения у "врага"
            move_wrap(enemy[0], direction)  # произвести  перемещение
        check_move()
    if k == 2:
        k += 2
    if k < 3:
        k += 1


k = 3
s = []
step = 60
N_X = 10
N_Y = 10
master = tkinter.Tk()
label = tkinter.Label(master, text="Найди выход")
label.pack()
player_pic = tkinter.PhotoImage(file="player.gif")
exit_pic = tkinter.PhotoImage(file="exit.gif")
fire_pic = tkinter.PhotoImage(file="fire.gif")
enemy_pic = tkinter.PhotoImage(file="enemy.gif")
canvas = tkinter.Canvas(master, bg='blue',
                        height=N_X * step, width=N_Y * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()
