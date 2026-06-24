import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Automatically load the hidden .env file
load_dotenv() 

client = genai.Client()

def generate_ai_commentary(batter, bowler, ball_outcome, over_num, ball_num, max_retries=2):
    sys_instruct = """You are an energetic, world-class cricket radio commentator.
    Your job is to write EXACTLY ONE sentence of thrilling, dramatic live commentary.
    CRITICAL RULE: You must base your excitement strictly on the provided 'Match Outcome'. Never change the runs scored.
    
    HOW TO BE DRAMATIC:
    - If Outcome is 'Dot': Describe a fierce delivery, a close miss, or a rock-solid defensive block.
    - If Outcome is '1 Run' or '2 Runs': Describe desperate running, a sharp throw from the deep, or a smart push into the gaps.
    - If Outcome is '4 Runs': Describe a cracking shot, piercing the field, racing to the ropes.
    - If Outcome is '6 Runs': Describe a massive, colossal hit, soaring into the stands.
    - If Outcome is 'Wicket': Describe the stumps flying, a spectacular diving catch, or the crowd erupting."""
    
    user_prompt = f"Bowler: {bowler}\nBatter: {batter}\nMatch Outcome: {ball_outcome}"
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct,
                    temperature=0.5,
                )
            )
            return response.text.strip()
            
        except Exception as e:
            error_msg = str(e)
            
            # Catch Rate Limits
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"   [API Traffic Jam] Reached rate limit. Waiting 60 seconds...")
                time.sleep(60) 
                
            # Catch Server Traffic
            elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                print(f"   [Server Busy] Google is overloaded. Retrying in 2 seconds...")
                time.sleep(2)
                
            # Unknown Errors
            else:
                return f"[API ERROR]: {error_msg}"
                
    return f"[System Fallback]: {bowler} to {batter}, result is {ball_outcome}."
