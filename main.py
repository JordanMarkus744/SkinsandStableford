from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Dict, List
import uvicorn
import sqlite3
from pythonFiles import calculate_stableford, update_handicap, calculate_skins, get_skins_money

app = FastAPI()

# Establish a database connection for use in functions
def get_db():
    conn = sqlite3.connect("golf_stats.db")
    try:
        yield conn
    finally:
        conn.close()

class Scores(BaseModel):
    scores: Dict[int, List[int]]  # Key is golfer_id, value is list of scores
    money: int
    course_id: int
    game_type: bool  # 0 for Stableford, 1 for Skins

@app.post("/input-scores")
def input_scores(game_data: Scores, conn: sqlite3.Connection = Depends(get_db)):
    if game_data.game_type:  # If it's a skins game
        skins_points = get_skins(Skins(scores=game_data.scores, money=game_data.money, course_id=game_data.course_id), conn)
        money_distribution: Dict[int, float] = get_skins_money(skins_points)
        return {"skins_points": skins_points, "money": money_distribution}

class Skins(BaseModel):
    scores: Dict[int, List[int]]  # Key is golfer_id, value is list of scores
    money: int
    course_id: int

def get_skins(round_data: Skins, conn: sqlite3.Connection):
    points = calculate_skins(round_data.scores, round_data.course_id, conn, round_data.money)
    return points  # Dictionary: {golfer_id: skins_won}

class Stableford(BaseModel):
    golfer_id: int  # Player's ID
    scores: List[int]  # Player's scores per hole
    course_id: int  # Course ID to get pars per hole

@app.post("/stableford")
def get_stableford_points(round_data: Stableford):
    points = calculate_stableford(round_data.scores, round_data.course_id)  # Calculate Stableford points
    difference = update_handicap(round_data.golfer_id, points)  # Update golfer's handicap
    return {"stableford_points": points, "difference": difference}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

