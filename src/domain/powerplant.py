from dataclasses import dataclass


@dataclass
class Powerplant:
    name: str
    fuel_cost: float
    type: str  # Not even really necessary, we never use this after initialization
    efficiency: float
    pmin: int
    pmax: int
    use: int = 0

    def __post_init__(self):
        if self.pmin > self.pmax:
            raise ValueError("pmin cannot be greater than pmax")

        if self.pmin < 0 or self.pmax < 0:
            raise ValueError("pmin and pmax must both be nonnegative")

    def get_mwh_cost(self):
        return self.fuel_cost / self.efficiency
