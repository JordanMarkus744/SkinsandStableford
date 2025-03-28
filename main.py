from fastapi import FastAPI
from pydantic import BaseModel
from pythonFiles import *


app = FastAPI()

class Stableford(BaseModel):
    golfer_id: int    # Player's id
    scores: list[int] # Player's scores per hole
    course_id: int    # course id to get pars per hole

@app.post("/stableford")
def get_stableford_points(round_data: Stableford):
    points = calculate_stableford(round_data.scores, round_data.course_id)
    
    return {"stableford_points": points}

