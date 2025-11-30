import random

class Wumpus:

    def __init__(self, size: int = 4):
        self.size = size
        self.reset()

    def reset(self):
        self.world = [['' for x in range(self.size)] for i in range(self.size)]
        self.pits = []
        self.wp_pos = None
        self.gold_pos = None

        self.alive = True
        self.won = False
        self.has_gold = False
        self.agent_pos = (0,0)
        # agent direction i decided right=0, down=1, left=2, up=3
        self.agent_dir = 0 
        self.score = 0
        self.visited = [[False] * self.size for i in range(self.size)]
        self.safe = [[False] * self.size for i in range(self.size)]
        self.danger = [[False] * self.size for i in range(self.size)]
        self.log = ["Gaem started. Agent is at (1,1)"]


    def generate_world(self):
        # wumppus position
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x,y) != (0,0):
                self.world[y][x] = "W"
                self.wp_pos = (x,y)
                break

        # gold pos
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x,y) not in [(0,0), self.wp_pos]:
                self.world[y][x] = "G"
                self.gold_pos = (x,y)
                break

        for x in range(self.size-1):
            for y in range(self.size-1):
                if (x,y) not in [(0,0), self.wp_pos, self.gold_pos]:
                    self.pits.append((x,y))

    def enter_cell(self):
        pass

    def has_adjacent_pit(self):
        pass


    def has_adjacent_wp(self):
        pass

    def infer_knowledge(self):
        pass

    def get_adjacent(self):
        pass

    def ai_step(self):
        pass

    def a_star(self):
        pass

    def move_to(self):
        pass

    def get_full_state(self):
        pass

