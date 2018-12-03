import random

class Frogsweeper:

    def __init__(self, n, m):
        self.situation = True
        self.area = sum([[sum([[' '] for a in range(n)], [])] for b in range(n)], [])
        self.n = n
        self.m = m

    def __str__(self):
        re = ''
        for row in self.area:
            for point in row:
                if isinstance(point, int) or point == '#':
                    re = re + str(point) + ' '
                elif point == 'F'or point == 'f':
                    re = re + 'P' + ' '
                else:
                    re = re + '# '
            re = re + '\n'
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
                if isinstance(point,str) and point in '012345678*f':
                    return False
        return True




if __name__ == '__main__':
    game = Frogsweeper(5, 1)
    game.initial()
    print(game)
    while game.situation and not game.has_won():
        move_a = 'a'
        move_b = 'b'
        while not move_a.isnumeric() or int(move_a) < 0 or int(move_a) > game.n - 1 :
            move_a = input("Please input a : ")
        while not move_b.isnumeric() or int(move_b) < 0 or int(move_b) > game.n - 1:
            move_b = input("Please input b : ")
        move = (int(move_a), int(move_b))
        click_or_flag = input("Do you want a click or flag('c' or 'f') : ")
        while click_or_flag != 'c' and click_or_flag != 'f':
            click_or_flag = input("Do you want a click or flag('c' or 'f') : ")
        if click_or_flag == 'c':
            game.area = game.make_click(move)
        if click_or_flag == 'f':
            game.area = game.make_flag(move)
        print(game)
    if game.situation:
        print("You win!")
    else:
        print("You lose!")

