from dataclasses import dataclass


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
    # todo: maybe implement stuff for eent resources
