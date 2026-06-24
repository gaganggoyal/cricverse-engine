import pandas as pd

def extract_player_profile(csv_filepath, player_name):
    print(f"Loading match data for {player_name}...")
    
    # 1. Load the Cricsheet CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_filepath)

    # 2. Filter the massive sheet to ONLY show balls where our player was batting
    player_data = df[df['striker'] == player_name]

    if player_data.empty:
        return f"Error: {player_name} not found in this dataset. Check spelling. (Try 'V Kohli' or 'RG Sharma')"

    # 3. Calculate Total Runs (Only counting runs off the bat)
    total_runs = player_data['runs_off_bat'].sum()

    # 4. Calculate Balls Faced (Excluding wides)
    # In Cricsheet, if 'wides' is empty (NaN) or 0, it counts as a legal delivery.
    valid_balls = player_data[player_data['wides'].isna() | (player_data['wides'] == 0)]
    balls_faced = len(valid_balls)

    # 5. Calculate the Strike Rate
    if balls_faced > 0:
        strike_rate = (total_runs / balls_faced) * 100
    else:
        strike_rate = 0.0

    # 6. Output the structured JSON profile
    profile = {
        "player_id": player_name.lower().replace(" ", "_"),
        "name": player_name,
        "runs": int(total_runs),
        "balls_faced": int(balls_faced),
        "strike_rate": round(strike_rate, 2)
    }
    
    return profile

# --- RUN THE TEST ---
# Replace '1001349.csv' with whatever filename you saw when you ran the 'ls' command earlier
# You will also need to change 'V Kohli' to a player who actually played in that specific match
result = extract_player_profile('t20_data/1001351.csv', 'V Kohli')
print(result)
