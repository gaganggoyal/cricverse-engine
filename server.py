from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json
import os

app = FastAPI()

# Allow your Netlify website to talk to your Render backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE REALISTIC PHYSICS ENGINE ---
def calculate_realistic_outcome(batter_name, bowler_name):
    # 1. Load the player database from the JSON file
    try:
        with open("players.json", "r") as file:
            database = json.load(file)
    except Exception:
        # Fallback if file is missing
        database = {"batters": {}, "bowlers": {}}

    # 2. Get ratings (Default to 50 if player isn't found)
    bat_rating = database["batters"].get(batter_name, {"rating": 50})["rating"]
    bowl_rating = database["bowlers"].get(bowler_name, {"rating": 50})["rating"]

    # 3. Calculate advantage
    advantage = bat_rating - bowl_rating
    outcomes = ["Dot", "1", "2", "3", "4", "6", "Wicket"]
    
    # Default balanced weights
    weights = [35, 30, 10, 2, 10, 8, 5]

    # Shift the odds based on the matchup!
    if advantage > 20:     # Mismatch favoring batter (e.g., Tendulkar vs Part-Timer)
        weights = [15, 25, 15, 2, 25, 17, 1] 
    elif advantage < -20:  # Mismatch favoring bowler (e.g., Tailender vs Bumrah)
        weights = [50, 20, 5, 0, 3, 1, 21]

    return random.choices(outcomes, weights=weights, k=1)[0]


@app.get("/api/bowl")
async def bowl_delivery():
    # Choose who is playing this ball (You can change these names to test!)
    current_batter = "S Tendulkar"
    current_bowler = "Part-Timer"
    
    # Calculate outcome using our smart engine
    math_outcome = calculate_realistic_outcome(current_batter, current_bowler)
    
    # placeholder AI commentary until you plug your Gemini code back here
    mock_commentary = f"{current_bowler} bowls to {current_batter}, and the result is a {math_outcome}!"
    
    return {
        "game_over": False,
        "batter": current_batter,
        "bowler": current_bowler,
        "pitch": "Standard",
        "math_outcome": math_outcome,
        "ai_commentary": mock_commentary,
        "current_score": "12/0",
        "current_over": "1.4"
    }