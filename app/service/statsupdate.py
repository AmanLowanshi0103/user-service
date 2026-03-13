def update_team_stats(home_stats, away_stats, home_goals, away_goals):

    # played matches
    home_stats.played += 1
    away_stats.played += 1

    # goals
    home_stats.goals_for += home_goals
    home_stats.goals_against += away_goals

    away_stats.goals_for += away_goals
    away_stats.goals_against += home_goals

    # result logic
    if home_goals > away_goals:

        home_stats.wins += 1
        away_stats.losses += 1
        home_stats.points += 3

    elif away_goals > home_goals:

        away_stats.wins += 1
        home_stats.losses += 1
        away_stats.points += 3

    else:

        home_stats.draws += 1
        away_stats.draws += 1

        home_stats.points += 1
        away_stats.points += 1