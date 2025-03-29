from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from pythonFiles import calculate_stableford, update_handicap, calculate_skins


app = FastAPI()

class Skins(BaseModel):
    scores: Dict[int, List[int]] # key is golfer id, and the list[int] is a list of scores for the golfer
    money: int
    course_id: int

@app.post("/skins")
def get_skins(round_data: Skins):
    points = calculate_skins(round_data.scores, round_data.course_id, round_data.money)
    return {"skins_points": points} # points should be a dictionary key being golfer_id and value being amount of skins won



class Stableford(BaseModel):
    golfer_id: int    # Player's id
    scores: List[int] # Player's scores per hole
    course_id: int    # course id to get pars per hole

@app.post("/stableford")
def get_stableford_points(round_data: Stableford): # takes in golfer_id, scores, course_id
    points = calculate_stableford(round_data.scores, round_data.course_id) # calculates stableford points and returns it
    update_handicap(round_data.golfer_id, points) # updates golfers handicap
    return {"stableford_points": points}

