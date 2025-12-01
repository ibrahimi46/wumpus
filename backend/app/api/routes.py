from fastapi import APIRouter
from ..core.game import Wumpus

router = APIRouter()
game = Wumpus(size=4)

@router.post("/new-game")
async def new_game():
    game.reset()
    return game.get_full_state()


@router.post("/ai-move")
async def ai_move():
    if not game.alive or game.won:
        return game.get_full_state()
    
    game.ai_step()
    return game.get_full_state()