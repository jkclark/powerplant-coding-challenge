from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.application.services.calculate_powerplant_use import calculate_powerplant_use
from src.domain.powerplant import Powerplant

app = FastAPI()


# Found this here: https://stackoverflow.com/a/66186106/3801865
class Fuels(BaseModel):
    gas: float = Field(..., alias="gas(euro/MWh)")
    kerosine: float = Field(..., alias="kerosine(euro/MWh)")
    co2: int = Field(..., alias="co2(euro/ton)")
    wind: int = Field(..., alias="wind(%)")

    def __getitem__(self, item):
        return getattr(self, item)


class PowerplantInfo(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int


class Payload(BaseModel):
    load: int
    fuels: Fuels
    powerplants: list[PowerplantInfo]


powerplant_type_to_fuel = {
    "gasfired": "gas",
    "turbojet": "kerosine",
    "windturbine": "wind",
}


@app.post("/productionplan")
async def productionplan(payload: Payload):
    powerplants = []
    for powerplant_info in payload.powerplants:
        fuel_cost = payload.fuels[powerplant_type_to_fuel[powerplant_info.type]]
        max_output = powerplant_info.pmax

        # Windturbines don't have fuel cost, and their actual max output
        # is dependent on the wind percentage
        if powerplant_info.type == "windturbine":
            fuel_cost = 0
            max_output = round(payload.fuels.wind / 100 * powerplant_info.pmax, 1)

        # Create powerplant
        powerplant = Powerplant(
            powerplant_info.name,
            fuel_cost,
            powerplant_info.type,
            powerplant_info.efficiency,
            powerplant_info.pmin,
            max_output,
        )

        # Add it to list of powerplants
        powerplants.append(powerplant)

    return calculate_powerplant_use(payload.load, powerplants)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
