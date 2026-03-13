def generate_round_robin(team_ids):

    if len(team_ids) % 2 != 0:
        team_ids.append(None)

    n = len(team_ids)
    rounds = n - 1
    fixtures = []

    teams = list(team_ids)

    for round_num in range(rounds):

        matchday = round_num + 1

        for i in range(n // 2):

            home = teams[i]
            away = teams[n - 1 - i]

            if home and away:
                fixtures.append({
                    "matchday": matchday,
                    "home_team_id": home,
                    "away_team_id": away
                })

        teams.insert(1, teams.pop())

    second_half = []

    for f in fixtures:
        second_half.append({
            "matchday": f["matchday"] + rounds,
            "home_team_id": f["away_team_id"],
            "away_team_id": f["home_team_id"]
        })

    fixtures.extend(second_half)

    return fixtures