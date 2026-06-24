from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json
import os

app = FastAPI()
# --- THE GAME MEMORY ---
match_state = {
    "runs": 0,
    "wickets": 0,
    "balls": 0
}

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
    # 1. Stop the game if 10 wickets fall (Your exact code!)
    if match_state["wickets"] >= 10:
        return {
            "game_over": True,
            "message": f"Innings Over! Final Score: {match_state['runs']}/{match_state['wickets']}"
        }

    # 2. Choose who is playing this ball
    current_batter = "S Tendulkar"
    current_bowler = "Part-Timer"
    
    # 3. Calculate outcome using our smart engine
    math_outcome = calculate_realistic_outcome(current_batter, current_bowler)
    
    # 4. UPDATE THE SCOREBOARD
    match_state["balls"] += 1
    if math_outcome == "Wicket":
        match_state["wickets"] += 1
    elif math_outcome != "Dot":
        # If it's a number (1, 2, 3, 4, 6), add it to runs
        match_state["runs"] += int(math_outcome)
        
    # Calculate Overs (e.g., 14 balls = 2.2 overs)
    overs_completed = match_state["balls"] // 6
    balls_in_current_over = match_state["balls"] % 6
    formatted_overs = f"{overs_completed}.{balls_in_current_over}"
    formatted_score = f"{match_state['runs']}/{match_state['wickets']}"

    # 5. Placeholder Commentary
    mock_commentary = f"{current_bowler} bowls to {current_batter}, and it's a {math_outcome}!"
    
    return {
        "game_over": False,
        "batter": current_batter,
        "bowler": current_bowler,
        "pitch": "Standard",
        "math_outcome": math_outcome,
        "ai_commentary": mock_commentary,
        "current_score": formatted_score,
        "current_over": formatted_overs
    }

@app.post("/api/reset")
async def reset_match():
    # Reset our global memory bank back to zero
    match_state["runs"] = 0
    match_state["wickets"] = 0
    match_state["balls"] = 0
    
    return {"message": "Memory wiped. New match started!"}