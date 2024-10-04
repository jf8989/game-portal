from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time
import json

app = FastAPI()

# Game state
secret_number = None
attempts = 0
start_time = 0
high_scores = {"Easy": 999, "Medium": 999, "Hard": 999}

class GameSettings(BaseModel):
    difficulty: str
    min_value: int = 1
    max_value: int = 100

class Guess(BaseModel):
    guess: int

def load_high_scores():
    try:
        with open("high_scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"Easy": 999, "Medium": 999, "Hard": 999}

def save_high_scores():
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)

@app.on_event("startup")
async def startup_event():
    global high_scores
    high_scores = load_high_scores()

@app.post("/start-game/")
def start_game(settings: GameSettings):
    global secret_number, attempts, start_time, high_scores
    if settings.difficulty == "Easy":
        settings.min_value, settings.max_value = 1, 100
    elif settings.difficulty == "Medium":
        settings.min_value, settings.max_value = 1, 500
    elif settings.difficulty == "Hard":
        settings.min_value, settings.max_value = 1, 1000
    
    if settings.min_value >= settings.max_value:
        raise HTTPException(status_code=400, detail="Invalid range. Minimum value must be less than maximum value.")

    secret_number = random.randint(settings.min_value, settings.max_value)
    attempts = 0
    start_time = time.time()
    return {"message": f"Game started! Guess the number between {settings.min_value} and {settings.max_value}."}

@app.post("/guess/")
def guess_number(guess: Guess):
    global attempts, secret_number, start_time, high_scores
    if secret_number is None:
        raise HTTPException(status_code=400, detail="Game not started. Please start a new game first.")

    attempts += 1
    if guess.guess < secret_number:
        return {"result": "Too low!", "attempts": attempts}
    elif guess.guess > secret_number:
        return {"result": "Too high!", "attempts": attempts}
    else:
        end_time = time.time()
        elapsed_time = int(end_time - start_time)
        message = f"Congratulations! You guessed the number in {attempts} attempts and {elapsed_time} seconds."
        
        # Update high scores
        difficulty = "Easy" if secret_number <= 100 else "Medium" if secret_number <= 500 else "Hard"
        if attempts < high_scores[difficulty]:
            high_scores[difficulty] = attempts
            save_high_scores()
            message += f" New high score for {difficulty} level!"
        
        return {"result": message, "attempts": attempts, "success": True}

@app.get("/high-scores/")
def get_high_scores():
    return high_scores