import random
import time

def calculate_ball_probability(batter_sr, bowler_econ, pitch):
    # Baseline probabilities out of 1000 points
    probabilities = {
        "Dot": 350,
        "1 Run": 380,
        "2 Runs": 100,
        "4 Runs": 90,
        "6 Runs": 50,
        "Wicket": 30
    }

    # Adjust for high-impact batters
    if batter_sr > 140:
        probabilities["6 Runs"] += 40
        probabilities["4 Runs"] += 30
        probabilities["Dot"] -= 70
    elif batter_sr < 110:
        probabilities["Dot"] += 40
        probabilities["4 Runs"] -= 20
        probabilities["6 Runs"] -= 20

    # Adjust for elite defensive bowlers
    if bowler_econ < 7.0:
        probabilities["Dot"] += 50
        probabilities["Wicket"] += 15
        probabilities["4 Runs"] -= 35
        probabilities["6 Runs"] -= 30

    # Environmental Modifiers (Stadium/Pitch Impact)
    if pitch == "Green Top":
        probabilities["Wicket"] += 20
        probabilities["Dot"] += 30
        probabilities["4 Runs"] -= 30
        probabilities["6 Runs"] -= 20
    elif pitch == "Batting Paradise":
        probabilities["6 Runs"] += 30
        probabilities["4 Runs"] += 40
        probabilities["Dot"] -= 50
        probabilities["Wicket"] -= 10

    # Prevent negative weights
    outcomes = list(probabilities.keys())
    weights = [max(0, w) for w in probabilities.values()]
    
    return outcomes, weights

def simulate_innings(batter, batter_sr, bowler, bowler_econ, pitch, max_overs=1):
    outcomes, weights = calculate_ball_probability(batter_sr, bowler_econ, pitch)
    
    total_runs = 0
    balls_faced = 0
    total_balls = max_overs * 6
    
    print("=" * 50)
    print(f"🏏 CRICVERSE SIMULATION: {pitch.upper()} PITCH")
    print(f"Batter: {batter} (SR: {batter_sr}) | Bowler: {bowler} (Econ: {bowler_econ})")
    print("=" * 50)
    
    # Live simulation loop
    for ball_count in range(1, total_balls + 1):
        # Calculate current over notation (e.g., 0.1, 0.2... 1.0)
        current_over = (ball_count - 1) // 6
        current_ball = (ball_count - 1) % 6 + 1
        
        # Roll the outcome
        result = random.choices(outcomes, weights=weights, k=1)[0]
        balls_faced += 1
        
        # Print the ball event with a slight time delay for realism
        time.sleep(0.5) 
        print(f"Over {current_over}.{current_ball} | {bowler} to {batter} -> {result}")
        
        if result == "Wicket":
            print("\n🔴 OUT! The bowling side celebrates!")
            break
        else:
            # Extract run value from string (e.g., "4 Runs" -> 4)
            if "Run" in result:
                runs = int(result.split()[0])
                total_runs += runs

    print("=" * 50)
    print(f"💥 FINAL SCORE: {batter} scored {total_runs} off {balls_faced} balls.")
    print("=" * 50)

