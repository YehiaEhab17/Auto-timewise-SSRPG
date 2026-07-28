from math import floor

from classes import LocationStats


def get_max_runs(loc: LocationStats, star_levels, player_level):

    max_unlocked = star_levels[loc.name]
    star_diff = max_unlocked - loc.stars
    max_hp = player_level + 20
    max_chests = player_level * 5 + 100
    # todo : check also current amount of chests

    guarantee = 0
    if star_diff >= 3:
        guarantee = 1
    elif star_diff == 2:
        guarantee = 2 / 3
    elif star_diff == 1:
        guarantee = 1 / 3

    chests_per_run = get_chests_per_run(loc)
    if loc.net_hp >= 0:
        runs_before_death = max_chests
    else:
        runs_before_death = max_hp // abs(loc.net_hp)

    chests = floor(guarantee * max_chests)

    runs = min(max(chests, runs_before_death * chests_per_run), 400)

    return runs


def get_completion_time(time, loops, chests_per_run=1):
    OROBOROUS_FRAMES = 118
    CHEST_FRAMES = 36

    time_seconds = time / 30
    treasures = loops * chests_per_run

    total_seconds = (
        time_seconds * loops
        + (OROBOROUS_FRAMES / 30) * (loops - 1)
        + (CHEST_FRAMES / 30) * treasures
    )

    return total_seconds


def get_chests_per_run(loc):
    if loc.name == "caustic_caves" and loc.stars >= 5 and loc.stars <= 15:
        return 2
    else:
        return 1

    # event logic too
