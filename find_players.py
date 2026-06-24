import pandas as pd
import glob
import os

def find_all_unique_players(folder_path):
    print(f"Scanning all CSV matches in {folder_path}...")
    
    # Get a list of all CSV files in the folder
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    unique_players = set()
    
    # Loop through every single match file
    for i, file in enumerate(all_files):
        try:
            # Read just the 'striker' and 'bowler' columns to save memory
            df = pd.read_csv(file, usecols=['striker', 'bowler'])
            
            # Add the names to our set (a set automatically removes duplicates)
            unique_players.update(df['striker'].dropna().unique())
            unique_players.update(df['bowler'].dropna().unique())
            
            # Print an update every 100 files so you know it hasn't frozen
            if (i + 1) % 100 == 0:
                print(f"Scanned {i + 1} matches...")
                
        except Exception as e:
            print(f"Skipping {file} due to error: {e}")

    # Sort the names alphabetically
    sorted_players = sorted(list(unique_players))
    
    # Save the massive list to a text file
    with open("all_players.txt", "w") as f:
        for player in sorted_players:
            f.write(f"{player}\n")
            
    print(f"\nSuccess! Found {len(sorted_players)} unique players.")
    print("Saved all names to 'all_players.txt'")

# --- RUN THE SCAN ---
find_all_unique_players('t20_data')
