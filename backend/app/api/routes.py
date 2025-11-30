from fastapi import APIRouter
from core.game import Wumpus

router = APIRouter()
game = Wumpus(size=4)

@router.get("/new-game")
def new_game():
    pass


@router.get("/ai-move")
def ai_move():
    if game.finished or game.won:
        return game.get_full_stats()
    
    game.ai_move
    return game.get_full_stats()