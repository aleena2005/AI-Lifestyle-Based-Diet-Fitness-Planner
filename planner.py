def build_prompt(data):
    # This prompt structure forces the AI to use the exact keys your app.py splits on
    return f"""
    Create a highly specific Wellness Plan for a {data['age']} year old {data['category']}.
    
    USER DETAILS:
    - Schedule: {data['schedule']}
    - Sleep: {data['sleep']}
    - Activity Level: {data['activity']}
    - Time for Workout: {data['workout_time']}
    - Diet: {data['food_type']} ({data['budget']} budget)
    - Health Goal: {data['goal']}
    - Restrictions: {data['restrictions']}

    REQUIRED FORMAT:
    You must start with "DIET PLAN:", then "WORKOUT PLAN:", then "DAILY ROUTINE ADVICE:".
    Do not use extra bolding on these three specific headers.

    DIET PLAN:
    (Provide meals here)

    WORKOUT PLAN:
    (Provide exercises here)

    DAILY ROUTINE ADVICE:
    (Provide lifestyle tips here)
    """