import random
import copy
from tkinter import *


class FrogSweeper:

    def __init__(self, n, m):
        self.situation = True
        self.area = sum([[sum([[' '] for a in range(n)], [])] for b in range(n)], [])
        self.n = n
        self.m = m

    def __str__(self):
        re = ''
        for row in self.area:
            for point in row:
                if isinstance(point, int) or point == '$':
                    re = re + str(point) + ' '
                elif point == 'F'or point == 'f':
                    re = re + 'P' + ' '
                else:
                    re = re + '# '
            re = re + '\n'
        return re

    def get_hiden_list(self):
        re = copy.deepcopy(self.area)
        for i in range(self.n):
            for j in range(self.n):
                if isinstance(self.area[i][j], int) or self.area[i][j] == '$':
                    re[i][j] = str(re[i][j])
                elif self.area[i][j] == 'F' or self.area[i][j] == 'f':
                    re[i][j] = 'P'
                else:
                    re[i][j] = '#'
        return re

    def find_neighbors(self, p):
        a = p[0]
        b = p[1]
        result = [(a - 1, b - 1), (a - 1, b), (a - 1, b + 1), (a, b - 1),
                  (a, b + 1), (a + 1, b - 1), (a + 1, b), (a + 1, b + 1)]
        re = []
        for point in result:
            if 0 <= point[0] <= self.n - 1 and 0 <= point[1] <= self.n - 1:
                re.append(point)
        return re

    def initial(self):
        li = []   # list of coordinate tuples containing mines
        for i in range(self.m):
            coor = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            while coor in li:
                coor = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            li.append(coor)
            self.area[coor[0]][coor[1]] = '*'  # '*' represents a mine.

        for a in range(self.n):
            for b in range(self.n):
                count = 0
                if self.area[a][b] != '*':
                    for point in self.find_neighbors((a, b)):
                        if self.area[point[0]][point[1]] == '*':
                            count += 1
                    self.area[a][b] = str(count)

    def find_zero(self, point):
        if self.area[point[0]][point[1]] != '0':
            self.area[point[0]][point[1]] = int(self.area[point[0]][point[1]])
            return []
        else:
            self.area[point[0]][point[1]] = 0
            return [point] + sum([self.find_zero(x) for x in self.find_neighbors(point)], [])

    def make_click(self, point):
        if self.area[point[0]][point[1]] == '0':
            self.find_zero(point)
        elif self.area[point[0]][point[1]] == '*':
            self.area[point[0]][point[1]] = '$'   # '$' means explosion.
            self.situation = False
        elif self.area[point[0]][point[1]] in "Ff":
            print("lv dicky")
        else:
            self.area[point[0]][point[1]] = int(self.area[point[0]][point[1]])
        return self.area

    def make_flag(self, point):
        if self.area[point[0]][point[1]] == '*':
            self.area[point[0]][point[1]] = 'F'
        elif self.area[point[0]][point[1]] == 'F' or self.area[point[0]][point[1]] == 'f':
            self.area[point[0]][point[1]] = '*'
        else:
            self.area[point[0]][point[1]] = 'f'
        return self.area

    def has_won(self):
        for row in self.area:
            for point in row:
                if isinstance(point, str) and point in '012345678*f':
                    return False
        return True


Frog = FrogSweeper(8, 8)
Frog.initial()


def create_board():
    row = []
    col = []
    for x in range(15):
        for y in range(15):
            row.append("0")
        col.append(row)
    return col


def count_time():
    global time_counts

    seconds = 0
    while True:
        seconds += 1
        print(seconds)
        time_counts["text"] = ""+seconds


def click_button(x, y):
    global buttons_list
    global face

    print(x)
    print(y)

    buttons_list[x][y]["text"] = "*"
    area = Frog.make_click((x, y))

    for x in range(len(buttons_list)):
        for y in range(len(buttons_list)):
            if Frog.get_hiden_list()[x][y] != "#":
                buttons_list[x][y]["text"] = Frog.get_hiden_list()[x][y]



def reset():
    global buttons_list

    for x in range(len(buttons_list)):
        for y in range(len(buttons_list)):
            buttons_list[x][y]["text"] = ""


def user_interface():
    global win
    global button
    global mine_counts
    global face
    global time_counts
    global buttons_list


    win = Tk()
    win.title("Frog Wrapper")

    """
    Top frame
    """
    f0 = Frame(win, padx=18, pady=4)
    f0.grid(row=1, column=1)

    mine_counts = Button(f0, text="000", width=4, height=2)
    mine_counts.grid(row=1, column=0)

    face = Button(f0, text="(*_*)", width=4, height=2, command=lambda: reset())
    face.grid(row=1, column=1)

    time_counts = Button(f0, text="000", width=4, height=2)
    time_counts.grid(row=1, column=2)

    """
    Bottom frame
    """
    f1 = Frame(win, padx=20, pady=20)
    f1.grid(row=2, column=1)

    buttons_list = []

    for x in range(Frog.n):

        row = []

        for y in range(Frog.n):
            button = Button(f1, text="", width=2, height=1, command=lambda click_x=x, click_y=y: click_button(click_x, click_y))
            button.grid(row=x, column=y)
            row.append(button)

        buttons_list.append(row)

    print(buttons_list)

    win.mainloop()


user_interface()


# if __name__ == '__main__':
#     game = FrogSweeper(5, 1)
#     game.initial()
#     print(game)
#     while game.situation and not game.has_won():
#         move_a = 'a'
#         move_b = 'b'
#         while not move_a.isnumeric() or int(move_a) < 0 or int(move_a) > game.n - 1 :
#             move_a = input("Please input a : ")
#         while not move_b.isnumeric() or int(move_b) < 0 or int(move_b) > game.n - 1:
#             move_b = input("Please input b : ")
#         move = (int(move_a), int(move_b))
#         click_or_flag = input("Do you want a click or flag('c' or 'f') : ")
#         while click_or_flag != 'c' and click_or_flag != 'f':
#             click_or_flag = input("Do you want a click or flag('c' or 'f') : ")
#         if click_or_flag == 'c':
#             game.area = game.make_click(move)
#         if click_or_flag == 'f':
#             game.area = game.make_flag(move)
#         print(game)
#     if game.situation:
#         print("You win!")
#     else:
#         print("You lose!")

