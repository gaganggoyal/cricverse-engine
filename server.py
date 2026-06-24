from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import simulate_match
import ai_commentary

app = FastAPI(title="Cricverse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# NEW: The "Memory" of our server
# ==========================================
match_state = {
    "runs": 0,
    "wickets": 0,
    "balls": 0
}

@app.get("/api/bowl")
def bowl_delivery():
    # Stop the game if 10 wickets fall
    if match_state["wickets"] >= 10:
        return {
            "game_over": True,
            "message": f"Innings Over! Final Score: {match_state['runs']}/{match_state['wickets']}"
        }

    batter = "V Kohli"
    batter_sr = 138.5
    bowler = "JJ Bumrah"
    bowler_econ = 6.4
    pitch = "Green Top"

    # 1. Math Engine
    outcomes, weights = simulate_match.calculate_ball_probability(batter_sr, bowler_econ, pitch)
    outcome = random.choices(outcomes, weights=weights, k=1)[0]

    # ==========================================
    # NEW: Update the Scorekeeper
    # ==========================================
    match_state["balls"] += 1
    
    if outcome == "Wicket":
        match_state["wickets"] += 1
    elif outcome == "1 Run":
        match_state["runs"] += 1
    elif outcome == "2 Runs":
        match_state["runs"] += 2
    elif outcome == "3 Runs":
        match_state["runs"] += 3
    elif outcome == "4 Runs":
        match_state["runs"] += 4
    elif outcome == "6 Runs":
        match_state["runs"] += 6

    # Calculate standard cricket overs (e.g., 1.4 overs)
    overs = match_state["balls"] // 6
    legal_balls = match_state["balls"] % 6
    over_display = f"{overs}.{legal_balls}"

    # 2. AI Engine (Now passing the real over numbers!)
    commentary = ai_commentary.generate_ai_commentary(batter, bowler, outcome, overs, legal_balls)

    # 3. Send the upgraded data package to the web
    return {
        "game_over": False,
        "batter": batter,
        "bowler": bowler,
        "pitch": pitch,
        "math_outcome": outcome,
        "ai_commentary": commentary,
        "current_score": f"{match_state['runs']}/{match_state['wickets']}",
        "current_over": over_display
    }
