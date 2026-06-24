import time
import random
import ai_commentary
import simulate_match

def start_match():
    print("=" * 60)
    print("🏏 CRICVERSE: BALL-BY-BALL DIAGNOSTIC 🏏")
    print("=" * 60)
    
    batter = "V Kohli"
    batter_sr = 138.5
    bowler = "JJ Bumrah"
    bowler_econ = 6.4
    pitch = "Green Top"
    
    # Get the probability matrix
    outcomes, weights = simulate_match.calculate_ball_probability(batter_sr, bowler_econ, pitch)
    
    for ball in range(1, 7):
        print(f"\n--- Over 0.{ball} ---")
        
        # 1. Math calculates the exact outcome
        outcome = random.choices(outcomes, weights=weights, k=1)[0]
        print(f"📊 Math Engine Output : {outcome}")
        
        # 2. AI generates the text based strictly on that outcome
        commentary = ai_commentary.generate_ai_commentary(batter, bowler, outcome, 0, ball)
        print(f"🎙️ AI Broadcaster     : {commentary}")
        
        # Pause to prevent API rate limits
        if ball < 6:
            time.sleep(4.5)

if __name__ == "__main__":
    start_match()
