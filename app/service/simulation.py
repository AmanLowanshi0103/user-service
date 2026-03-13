import random

def simulate_match(home_rating, away_rating):

    # home advantage
    home_power = home_rating + 3 + random.randint(0, 10)
    away_power = away_rating + random.randint(0, 10)

    if home_power > away_power:
        home_goals = random.randint(1, 3)
        away_goals = random.randint(0, 2)

    elif away_power > home_power:
        home_goals = random.randint(0, 2)
        away_goals = random.randint(1, 3)

    else:
        home_goals = away_goals = random.randint(0, 2)

    return home_goals, away_goals