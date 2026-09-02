from dataclasses import dataclass

LOCATION_NAMES = {
    "rocky_plateau": "Rocky Plateau",
    "deadwood_valley": "Deadwood Canyon",
    "caustic_caves": "Caves of Fear",
    "fungus_forest": "Mushroom Forest",
    "undead_crypt": "Haunted Halls",
    "bronze_mine": "Boiling Mine",
    "icy_ridge": "Icy Ridge",
    "temple": "Temple",
}

LOCATION_INDEX = {
    "rocky_plateau": 1,
    "deadwood_valley": 2,
    "caustic_caves": 3,
    "fungus_forest": 4,
    "undead_crypt": 5,
    "bronze_mine": 6,
    "icy_ridge": 7,
    "temple": 8,
}


EVENT_LOCATIONS = {
    "summer": "rocky_plateau",
    "halloween": "undead_crypt",
    "winter": "icy_ridge",
    "spring": "fungus_forest",
    "guardian_2x": "bronze_mine",
    "xyloalgia_2x": "deadwood_valley",
    "nagaraja_2x": "temple",
}


# {'id': 'caustic_caves3', 'bT': 1112.0, 'aT': 1811.661, 'aHl': 20.82896, 'aHg': 0.0, 'aKg': 13.34721, 'aXg': 17.55122, 'aRg': 154.8184, 'd': 754.3131}
@dataclass
class LocPlayerStats:
    loc_id: str  # loc id e.g caustic_caves3
    name: str
    stars: int
    bT: float  # best time in frames
    aT: float  # average time in frames
    aHl: float  # average health lost
    aHg: float  # average health gain
    net_hp: float
    aKg: float  # average ki gain
    aXg: float  # average xp gain?
    aRg: float  # average resource gain
    d: float  # damage?
    # TODO: maybe implement stuff for eent resources


@dataclass
class LocOfflineStats:
    loc_id: str
    name: str
    stars: int
    bT: float  # frames
    aT: float  # frames
    completed_in: float  # frames
    completed_in_best: float  # frames
    ends_in_death: bool
    loops: int
    chests_per_run: int
    value_per_clear: float  # from chest rates
    enchant_rate: float  # calculated based on speed
    # TODO: later stuff for emerald eggs, event resources, etc. things ppl might want
