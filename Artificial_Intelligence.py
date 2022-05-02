class ArtificialIntelligence:
    def __init__(self, width, height, board, player, actions):
        self.width = width
        self.height = height
        self.board = board
        self.player = player
        self.opponent = 3 - player
        self.actions = actions
        self.dist_opponent = self.calc_danger(player)
        self.dist_player = self.calc_danger(self.opponent)

    def get_move(self):
        min_dist = self.height * self.width
        ans = (-1, -1)
        corner_square = (-1, -1)
        # В первую очередь ставим новый квадрат (т.е. крепость) там,
        # где он будет иметь границу по стороне с существующим квадратом
        for i in range(self.width):
            for j in range(self.height):
                if self.dist_player[i][j] == 1:
                    if self.board[i][j] == self.opponent:
                        if i > 0:
                            if self.board[i - 1][j] == -self.player:
                                return i, j
                        if j > 0:
                            if self.board[i][j - 1] == -self.player:
                                return i, j
                        if i + 1 < self.width:
                            if self.board[i + 1][j] == -self.player:
                                return i, j
                        if j + 1 < self.height:
                            if self.board[i][j + 1] == -self.player:
                                return i, j
                        corner_square = (i, j)
                    if 2 < self.dist_opponent[i][j] < min_dist:
                        min_dist = self.dist_opponent[i][j]
                        ans = i, j
        # Новый квадрат (т.е. крепость) через угол от существующего
        if corner_square[0] != -1:
            return corner_square
        if 3 - self.actions % 3 > 1:
            for i in range(self.width):
                for j in range(self.height):
                    if self.dist_player[i][j] == 1:
                        if self.dist_opponent[i][j] == 1:
                            return i, j
        if ans[0] != -1:
            return ans
        for i in range(self.width):
            for j in range(self.height):
                if self.dist_player[i][j] == 1:
                    if self.dist_opponent[i][j] == 2:
                        return i, j
                    if self.dist_opponent[i][j] == 1:
                        ans = i, j
        if ans[0] != -1:
            return ans
        return None

    def calc_danger(self, player):
        opponent = 3 - player
        dist = [[-1] * self.height for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == opponent and dist[i][j] == -1:
                    self.dfs(i, j, opponent, dist)
        queue = []
        for i in range(self.width):
            for j in range(self.height):
                if dist[i][j] == 0:
                    queue.append((i, j))
        ind = 0
        while ind < len(queue):
            i, j = queue[ind][0], queue[ind][1]
            for del_i in range(-1, 2, 1):
                for del_j in range(-1, 2, 1):
                    if del_i != 0 or del_j != 0:
                        new_i = i + del_i
                        new_j = j + del_j
                        if 0 <= new_i < self.width and 0 <= new_j < self.height:
                            if dist[new_i][new_j] == -1:
                                if self.board[new_i][new_j] != -player:
                                    dist[new_i][new_j] = dist[i][j] + 1
                                    queue.append((new_i, new_j))
            ind += 1
        return dist

    def print_dist(self, dist):
        for j in range(self.height):
            for i in range(self.width):
                p = dist[i][j]
                if p == -1:
                    p = "."
                print(str(p), end="")
            print()
        print("-" * 15)

    def dfs(self, i, j, player, dist):
        dist[i][j] = 0
        for del_i in range(-1, 2, 1):
            for del_j in range(-1, 2, 1):
                if del_i != 0 or del_j != 0:
                    new_i = i + del_i
                    new_j = j + del_j
                    if 0 <= new_i < self.width and 0 <= new_j < self.height:
                        if dist[new_i][new_j] == -1:
                            if abs(self.board[new_i][new_j]) == player:
                                self.dfs(new_i, new_j, player, dist)
