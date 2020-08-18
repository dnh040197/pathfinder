class Algorithm:
    def __init__(self, board):
        self.board = board
        self.visited_node = {self.board.st: 0}
        self.path = []

    def run(self, weight, pos):
        ls0 = {(pos[0], pos[1] - 1): weight + 1,
               (pos[0], pos[1] + 1): weight + 1,
               (pos[0] + 1, pos[1]): weight + 1,
               (pos[0] - 1, pos[1]): weight + 1}
        tmp = []
        for k in ls0.keys():
            # If it's not a wall
            if self.board.matrix[k[0]][k[1]] != -1:
                # k visited
                if k in self.visited_node.keys():
                    # If the current weight <= the prev weight on this node
                    # Overwrite the node
                    if ls0[k] <= self.visited_node[k]:
                        self.visited_node.update({k: ls0[k]})
                    else:
                        tmp.append(k)

                # Update if k isn't visited
                else:
                    self.visited_node.update({k: ls0[k]})
            # If it's a wall, remember the key to it
            else:
                tmp.append(k)

        # Delete walls with the keys remembered
        for e in tmp:
            ls0.pop(e)

        return ls0

    def find_path(self, end_pos):
        if self.visited_node[end_pos] != 1:
            lst = [(end_pos[0], end_pos[1] - 1),
                   (end_pos[0], end_pos[1] + 1),
                   (end_pos[0] + 1, end_pos[1]),
                   (end_pos[0] - 1, end_pos[1])]
            for i in lst:
                if i in self.visited_node.keys():
                    if self.visited_node[i] == self.visited_node[end_pos] - 1:
                        self.path.append(i)
                        break

    def end_pos_found(self):
        return self.board.en in self.visited_node.keys()

    def reset(self, board):
        self.board = board
        self.visited_node = {self.board.st: 0}
        self.path = []

