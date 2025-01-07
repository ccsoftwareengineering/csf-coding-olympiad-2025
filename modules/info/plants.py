from enum import Enum


class PlantType(Enum):
    FOSSIL_FUEL = 'fossil fuel power station',
    SOLAR = 'solar power plant',
    WIND = 'wind farm',
    GEOTHERMAL = 'geothermal power plant',
    HYDROPOWER = 'hydroelectric power plant',
    NUCLEAR = 'nuclear power plant',


plants = {
    PlantType.FOSSIL_FUEL: {
        "cost": 500_000,
        "output_mw": 50,
        "pollution_tco2e": 150,
        "location_constraints": "None (Can be placed anywhere)",
        "description": "Generates reliable energy at a low upfront cost. However, it produces high levels of "
                       "pollution and contributes to environmental degradation.",
        "size": 10,
        "upkeep": 100_000
    },
    PlantType.SOLAR: {
        "cost": 750_000,
        "output_mw": 20,
        "pollution_tco2e": 0,
        "location_constraints": "Produces clean, renewable energy with minimal pollution. Its energy output is "
                                "limited and can fluctuate depending on weather conditions.",
        "size": 8,
        "upkeep": 50_000
    },
    PlantType.WIND: {
        "cost": 1_000_000,
        "output_mw": 30,
        "pollution_tco2e": 0,
        "location_constraints": "Provides renewable energy with zero emissions. Energy production is less predictable "
                                "and depends on wind availability.",
        "size": 30,
        "upkeep": 80_000
    },
    PlantType.GEOTHERMAL: {
        "cost": 1_500_000,
        "output_mw": 40,
        "pollution_tco2e": 5,
        "location_constraints": "Delivers consistent energy with minimal pollution. High initial costs make it an "
                                "expensive investment.",
        "size": 15,
        "upkeep": 150_000
    },
    PlantType.HYDROPOWER: {
        "cost": 2_000_000,
        "output_mw": 60,
        "pollution_tco2e": 2,
        "location_constraints": "Generates efficient, renewable energy with very low emissions. Its construction is "
                                "costly and requires significant infrastructure.",
        "size": 25,
        "upkeep": 200_000
    },
    PlantType.NUCLEAR: {
        "cost": 4_000_000,
        "output_mw": 100,
        "pollution_tco2e": 50,
        "location_constraints": "Offers a massive energy output and low greenhouse gas emissions. It comes with high "
                                "costs, radioactive waste, and safety concerns.",
        "size": 20,
        "upkeep": 500_000
    }
}
