import random
from collections import deque

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

        self.risk_meter = [[0.0 for x in range(self.size)] for i in range(self.size)]
        self.suspected_pits = [[False] * self.size for i in range(self.size)]
        self.suspected_wumpus = [[False] * self.size for i in range(self.size)]
        self.confirmed_safe = [[False] * self.size for i in range(self.size)]

        self.generate_world()
        self.confirmed_safe[0][0] = True
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

        for i in range(self.size - 1):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if (x,y) not in [(0,0), self.wp_pos, self.gold_pos] and (x,y) not in self.pits:
                    self.pits.append((x,y))
                    self.world[y][x] = "P"
                    break

    def has_adjacent_pit(self, x, y) -> bool:
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = dx+x, dy+y
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.world[ny][nx] == "P":
                    return True
                
        return False
    
    def has_adjacent_wp(self, x, y) -> bool:
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx , ny = dx+x, dy+y
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.world[ny][nx] == "W":
                    return True
            
        return False
    
    def get_perceptions(self, x: int, y: int):
        res = {"breeze": False, "stench": False, "glitter": False}
        
        if self.world[y][x] == "G": 
            res["glitter"] = True
            
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.world[ny][nx] == "P": res["breeze"] = True
                if self.world[ny][nx] == "W": res["stench"] = True
        return res

    def enter_cell(self, x, y):
        self.visited[y][x] = True
        self.safe[y][x] = True

        if self.world[y][x] == "P":
            self.alive = False
            self.score -= 1000
            
            return

        if self.world[y][x] == "W":
            self.alive = False
            self.score -= 1000
            
            return
        
        if self.world[y][x] == "G" and not self.has_gold:
            self.has_gold = True
            self.won = True
            self.score += 1000
            

        percepts = self.get_perceptions(x, y)
        
        p_str = []
        if percepts["breeze"]: p_str.append("BREEZE")
        if percepts["stench"]: p_str.append("STENCH")
        if percepts["glitter"]: p_str.append("GLITTER")

        self.infer_knowledge(x=x, y=y, percepts=percepts)

    def get_best_move(self):
        if not self.alive or self.won: return None
        
        candidates = []
        best_safe = None
        min_dist_safe = float('inf')

        frontier = set()
        for y in range(self.size):
            for x in range(self.size):
                if self.visited[y][x]:
                    for nx, ny in self.get_adjacent(x, y):
                        if not self.visited[ny][nx]:
                            frontier.add((nx, ny))


        for fx, fy in frontier:
        
            if self.confirmed_safe[fy][fx]:
        
                dist = abs(fx - self.agent_pos[0]) + abs(fy - self.agent_pos[1])
                if dist < min_dist_safe:
                    min_dist_safe = dist
                    best_safe = (fx, fy)
            
        
            candidates.append(((fx, fy), self.risk_meter[fy][fx]))

        
        if best_safe:
            return best_safe

        
        if candidates:
            candidates.sort(key=lambda x: x[1]) 
            return candidates[0][0]
            
        return None

    def infer_knowledge(self, x, y, percepts):
        self.visited[y][x] = True
        self.safe[y][x] = True
    
        if not percepts["breeze"] and not percepts["stench"]:
            for nx, ny in self.get_adjacent(x, y):
                self.confirmed_safe[ny][nx] = True
                self.risk_meter[ny][nx] = 0.0
                self.suspected_pits[ny][nx] = False
                self.suspected_wumpus[ny][nx] = False
        
        
        
        if percepts["breeze"]:
            for nx, ny in self.get_adjacent(x, y):
                if not self.visited[ny][nx] and not self.confirmed_safe[ny][nx]:
                    self.suspected_pits[ny][nx] = True
                    self.risk_meter[ny][nx] += 0.3

        
        if percepts["stench"]:
            for nx, ny in self.get_adjacent(x, y):
                if not self.visited[ny][nx] and not self.confirmed_safe[ny][nx]:
                    self.suspected_wumpus[ny][nx] = True
                    self.risk_meter[ny][nx] += 0.3
           
    def get_adjacent(self, x, y):
        adj = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adj.append((nx, ny))
        return adj

    def ai_step(self):
        target = self.get_best_move()
        if target:
            self.move_to(target)
        else:
            pass

    def a_star(self, start, goal):
        queue = deque([start])
        came = {start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            for nx, ny in self.get_adjacent(x, y):
                if (nx, ny) not in came and (self.safe[ny][nx] or (nx, ny) == goal):
                    came[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if goal not in came:
            return [start]

        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came[cur]
        path.reverse()

        return path
        
    def move_to(self, pos):
        dx = pos[0] - self.agent_pos[0]
        dy = pos[1] - self.agent_pos[1]

        if dx == 1: self.agent_dir = 0
        elif dy == 1: self.agent_dir = 1
        elif dx == -1: self.agent_dir = 2 
        elif dy == -1: self.agent_dir = 3  

        self.agent_pos = pos
        self.score -= 1
        self.enter_cell(*pos)

    def get_full_state(self):
        suggested_move = self.get_best_move()

        grid = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = {
                    "x": x, "y": y,
                    "visited": self.visited[y][x],
                    "agentHere": (x,y) == self.agent_pos,
                    
                    
                    "isSafe": self.confirmed_safe[y][x],
                    "isAiSuggestion": suggested_move == (x,y),
                    
                    
                    "breeze": self.visited[y][x] and any(self.world[ny][nx] == "P" for nx, ny in self.get_adjacent(x, y)),
                    "stench": self.visited[y][x] and any(self.world[ny][nx] == "W" for nx, ny in self.get_adjacent(x, y)),
                    "glitter": self.visited[y][x] and self.world[y][x] == "G",
                    
                    
                    "realPit": self.world[y][x] == "P",
                    "realWumpus": self.world[y][x] == "W",
                    "realGold": self.world[y][x] == "G",
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
        }