import re

from core.classes import LocOfflineStats, LocPlayerStats, LOCATION_INDEX


def get_location_times(stats):
    locations: dict[tuple[str, int], LocPlayerStats] = {}

    for location in stats:
        match = re.match(r"^([a-zA-Z_]+)(\d+)$", location["id"])

        if match:
            name, stars = match.groups()
        else:
            continue

        aHg_val = location.get("aHg", 0.0)
        aHl_val = location.get("aHl", 0.0)

        loc_stats = LocPlayerStats(
            loc_id=location["id"],
            name=name,
            stars=int(stars),
            bT=location.get("bT", 0.0),
            aT=location.get("aT", 0.0),
            aHl=aHl_val,
            aHg=aHg_val,
            net_hp=aHg_val - aHl_val,
            aKg=location.get("aKg", 0.0),
            aXg=location.get("aXg", 0.0),
            aRg=location.get("aRg", 0.0),
            d=location.get("d", 0.0),
        )
        locations[(name, int(stars))] = loc_stats
    return locations


def get_max_runs(loc: LocPlayerStats, star_levels, player_level, chests_per_run):

    max_unlocked = star_levels[loc.name]
    star_diff = max_unlocked - loc.stars
    max_hp = player_level + 20
    max_chests = player_level * 5 + 100
    # TODO: potions affect

    guarantee = 0
    if star_diff >= 3:
        guarantee = 1
    elif star_diff == 2:
        guarantee = 2 / 3
    elif star_diff == 1:
        guarantee = 1 / 3

    if loc.net_hp >= 0:
        runs_before_death = max_chests
    else:
        runs_before_death = max_hp // abs(loc.net_hp)

    chests = round(guarantee * max_chests)

    runs = min(max(chests, runs_before_death * chests_per_run), 400)

    return runs


def get_completion_time(time, loops, chests_per_run=1):
    OROBOROUS_FRAMES = 118
    CHEST_FRAMES = 36

    treasures = loops * chests_per_run

    total_frames = (
        (time * loops) + (OROBOROUS_FRAMES * (loops - 1)) + (CHEST_FRAMES * treasures)
    )

    return total_frames


def get_chests_per_run(loc, active_event):
    if loc.name == "caustic_caves" and loc.stars >= 5 and loc.stars <= 15:
        base = 2
    else:
        base = 1

    return base + 1 if loc.name == active_event else base


def get_offline_stats(
    locations, location_values, star_levels, player_level, active_event
):
    offline_stats_dict: dict[tuple[str, int], LocOfflineStats] = {}

    for loc in locations.values():
        if loc.stars < 5:
            continue  # chest rates only support 5* and up (and why would u offline 3* :p)

        loc_id = loc.loc_id
        bT = loc.bT
        aT = loc.aT

        chests_per_run = get_chests_per_run(loc, active_event)
        loops = get_max_runs(loc, star_levels, player_level, chests_per_run)
        ends_in_death = loops != 100 + 5 * player_level
        completed_in = get_completion_time(aT, loops, chests_per_run)
        completed_in_best = get_completion_time(bT, loops, chests_per_run)

        if loc_id not in location_values:
            print(f"skipping {loc_id}")
            continue
        value_per_clear = location_values[loc_id]
        enchant_rate = (value_per_clear * loops) / (completed_in / 30)
        enchant_rate_best = (value_per_clear * loops) / (completed_in_best / 30)

        offline_stats = LocOfflineStats(
            loc_id=loc_id,
            name=loc.name,
            stars=loc.stars,
            bT=bT,
            aT=aT,
            completed_in=completed_in,
            completed_in_best=completed_in_best,
            ends_in_death=ends_in_death,
            loops=loops,
            chests_per_run=chests_per_run,
            value_per_clear=value_per_clear,
            enchant_rate=enchant_rate,
            enchant_rate_best=enchant_rate_best,
        )
        offline_stats_dict[loc.name, int(loc.stars)] = offline_stats

    return offline_stats_dict


def sort_locs_by_rate(
    offline_stats_dict: dict[tuple[str, int], LocOfflineStats], best: bool
):
    return sorted(
        offline_stats_dict.values(),
        key=lambda loc: loc.enchant_rate if not best else loc.enchant_rate_best,
        reverse=True,
    )


def get_completion_time_table(
    offline_stats_dict: dict[tuple[str, int], LocOfflineStats],
    include_deaths: bool = False,
):

    completion_time_table = [["" for _ in range(32)] for _ in range(8)]

    # row, col : hour, min
    for (name, stars), stats in offline_stats_dict.items():
        if stats.ends_in_death and not include_deaths:
            continue
        hours, minutes = get_timewise_formatted_time(stats.completed_in)
        col = (stars - 5) * 2
        completion_time_table[LOCATION_INDEX[name] - 1][col] = hours
        completion_time_table[LOCATION_INDEX[name] - 1][col + 1] = minutes

    return format_table(completion_time_table)


def get_timewise_formatted_time(frames):
    total_seconds = frames // 30
    total_minutes = total_seconds // 60

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return hours, minutes


def format_table(table):
    lines = []
    for row in table:
        cells = [str(cell) for cell in row]
        lines.append("\t".join(cells))
    return "\n".join(lines)
