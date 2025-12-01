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

        self.generate_world()
        self.enter_cell(0,0)

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

        for x in range(self.size):
            for y in range(self.size-1):
                if (x,y) not in [(0,0), self.wp_pos, self.gold_pos]:
                    self.pits.append((x,y))

    def has_adjacent_pit(self, x, y) -> bool:
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = dx+x, dy+y
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.world[ny][nx] == "P":
                    return True
                
        return False
    
    def has_adjacent_wp(self, x, y) -> bool:
        for dx, dy in [(0,0), (0,1), (1,0), (-1,0)]:
            nx , ny = dx+x, dy+y
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.world[ny][nx] == "W":
                    return True
            
        return False
    
    def get_perceptions(self, x: int, y: int):
        p = set()
        if self.has_adjacent_pit(x, y):   p.add("breeze")
        if self.has_adjacent_wp(x, y):    p.add("stench")
        if self.world[y][x] == "G":       p.add("glitter")
        return p

    def enter_cell(self, x, y):
        self.visited[y][x] = True
        self.safe[y][x] = True

        if self.world[y][x] == "P":
            self.alive = False
            self.score -= 1000
            self.log.append("Fell into a pit. DEAD!")
            return

        if self.world[y][x] == "W":
            self.alive = False
            self.score -= 1000
            self.log.append("Eaten by wumpus. DEAD!")
            return
        

        perceptions = self.get_perceptions(x, y)
        if perceptions:
            self.log.append(",".join(perceptions))

        self.infer_knowledge()

    def infer_knowledge(self):
        changed = True
        while changed:
            changed = False
            for y in range(self.size):
                for x in range(self.size):
                    if not self.visited[y][x]:
                        continue

                    adj = self.get_adjacent(x, y)
                    perceptions = self.get_perceptions(x, y)
                    has_breeze = "breeze" in perceptions
                    has_stench = "stench" in perceptions

                    # if no breeze all adjcanet cells are safe
                    if not has_breeze:
                        for ax, ay in adj:
                            if not self.danger[ay][ax]:
                                if not self.safe[ay][ax]:
                                    self.safe[ay][ax] = True
                                    changed = True

                    # if its breeze with 3 safe neighbors its a pit
                    if has_breeze:
                        safe_neighbors = [(ax, ay) for ax, ay in adj if self.safe[ay][ax]]
                        if len(safe_neighbors) == len(adj) - 1:
                            for ax, ay in adj:
                                if not self.safe[ay][ax] and not self.danger[ay][ax]:
                                    self.danger[ay][ax] = True
                                    self.log.append(f"Inferred PIT at ({ax+1},{ay+1})")
                                    changed = True

                    # if stench adj are safe
                    if not has_stench:
                        for ax, ay in adj:
                            if not self.danger[ay][ax]:
                                if not self.safe[ay][ax]:
                                    self.safe[ay][ax] = True
                                    changed = True

                    if has_stench:
                        safe_neighbors = [(ax, ay) for ax, ay in adj if self.safe[ay][ax]]
                        if len(safe_neighbors) == len(adj) - 1:
                            for ax, ay in adj:
                                if not self.safe[ay][ax] and not self.danger[ay][ax]:
                                    self.danger[ay][ax] = True
                                    self.log.append(f"Inferred WUMPUS at ({ax+1},{ay+1})")
                                    changed = True

    def get_adjacent(self, x, y):
        adj = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adj.append((nx, ny))
        return adj

    def ai_step(self):
        if not self.alive or self.won: return

        # check for gold
        if self.has_gold:
            path = self.a_star((self.agent_pos[0], self.agent_pos[1]), (0,0))
            if len(path) > 1:
                self._move_to(path[1])
            else:
                self.won = True
                self.score += 1000
                self.log.append("CLIMBED OUT WITH GOLD — YOU WIN!")
            return

        # check safe and unvisited
        safe_unvisited = []
        for y in range(self.size):
            for x in range(self.size):
                if self.safe[y][x] and not self.visited[y][x]:
                    safe_unvisited.append((x, y))

        if safe_unvisited:
            target = min(safe_unvisited, key=lambda p: abs(p[0]-self.agent_pos[0]) + abs(p[1]-self.agent_pos[1]))
            path = self.a_star(self.agent_pos, target)
            if len(path) > 1:
                self.move_to(path[1])
        else:
            self.log.append("No safe moves — exploring visited...")

    def a_star(self, start, goal):
        return [start, goal]
        
    def move_to(self, pos):
        dx = pos[0] - self.agent_pos[0]
        dy = pos[1] - self.agent_pos[1]

        if dx == 1: self.agent_dir = 0
        elif dy == -1: self.agent_dir = 1
        elif dx == -1: self.agent_dir = 2
        elif dy == 1: self.agent_dir = 3

        self.agent_pos = pos
        self.score -= 1
        self.enter_cell(*pos)
        self.log.append(f"Moved to ({pos[0]+1},{pos[1]+1})")

    def get_full_state(self):
        grid = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = {
                    "x": x+1, "y": y+1,
                    "visited": self.visited[y][x],
                    "safe": self.safe[y][x],
                    "danger": self.danger[y][x],
                    "breeze": self.has_adjacent_pit(x, y),
                    "stench": self.has_adjacent_wp(x, y),
                    "glitter": self.world[y][x] == 'G',
                    "hasAgent": (x, y) == self.agent_pos,
                    "agentDir": ["right","down","left","up"][self.agent_dir],
                }
                row.append(cell)
            grid.append(row)

        return {
            "grid": grid,
            "score": self.score,
            "alive": self.alive,
            "hasGold": self.has_gold,
            "won": self.won,
            "gameOver": not self.alive or self.won,
            "logLines": self.log[-20:], 
        }

