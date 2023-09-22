import unittest

from src.application.services.calculate_powerplant_use import calculate_powerplant_use
from src.domain.powerplant import Powerplant


def test_calculate_powerplant_use():
    # Assemble
    load = 910
    powerplants = [
        Powerplant("gasfiredbig1", 13.4, "gasfired", 0.53, 100, 460),
        Powerplant("gasfiredbig2", 13.4, "gasfired", 0.53, 100, 460),
        Powerplant("gasfiredsomewhatsmaller", 13.4, "gasfired", 0.37, 40, 210),
        Powerplant("tj1", 50.8, "turbojet", 0.3, 0, 16),
        Powerplant("windpark1", 0, "windturbine", 1, 0, 90),
        Powerplant("windpark2", 0, "windturbine", 1, 0, 21.6),
    ]

    # Act
    result = calculate_powerplant_use(load, powerplants)

    # Assert
    case = unittest.TestCase()
    expected = [
        {"name": "gasfiredbig1", "p": 460},
        {"name": "gasfiredbig2", "p": 338.4},
        {"name": "gasfiredsomewhatsmaller", "p": 0.0},
        {"name": "tj1", "p": 0.0},
        {"name": "windpark1", "p": 90.0},
        {"name": "windpark2", "p": 21.6},
    ]
    case.assertCountEqual(result, expected)
