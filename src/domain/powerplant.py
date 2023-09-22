from dataclasses import dataclass


@dataclass
class Powerplant:
    name: str
    fuel_cost: float
    type: str  # Not even really necessary
    efficiency: float
    pmin: int
    pmax: int
    use: int = 0

    def get_mwh_cost(self):
        return self.fuel_cost / self.efficiency
