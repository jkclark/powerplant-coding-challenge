from typing import List

from src.domain.powerplant import Powerplant


def calculate_powerplant_use(load: int, powerplants: List[Powerplant]):
    # In order of cheapest to most expensive, use as much power as possible
    sorted_pps = sorted(powerplants, key=lambda pp: pp.get_mwh_cost())

    load_left = load
    for pp in sorted_pps:
        # If the load left is less than the minimum power, we can't use this powerplant
        if load_left < pp.pmin:
            continue

        # If the load left is less than the maximum power, we can only use the load left
        if load_left < pp.pmax:
            pp.use = load_left
            load_left = 0
            break

        # If the load left is greater than the maximum power, we can use the maximum power
        pp.use = pp.pmax
        load_left -= pp.pmax

    return [
        {
            "name": pp.name,
            "p": pp.use,
        }
        for pp in powerplants
    ]
