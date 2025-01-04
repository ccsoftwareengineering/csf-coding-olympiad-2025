from modules.more_utilities.enums import PlantType

power_plants = {
    PlantType.FOSSIL_FUEL: {
        "cost": 500_000,
        "output_mw": 50,
        "pollution_tco2e": 150,
        "location_constraints": "None (Can be placed anywhere)",
        "size": 10
    },
    PlantType.SOLAR: {
        "cost": 750_000,
        "output_mw": 20,
        "pollution_tco2e": 0,
        "location_constraints": "Requires open, non-shaded areas",
        "size": 8
    },
    PlantType.WIND: {
        "cost": 1_000_000,
        "output_mw": 30,
        "pollution_tco2e": 0,
        "location_constraints": "Requires areas with high wind potential",
        "size": 30
    },
    PlantType.GEOTHERMAL: {
        "cost": 1_500_000,
        "output_mw": 40,
        "pollution_tco2e": 5,
        "location_constraints": "Requires geothermal hotspot",
        "size": 15,
        "upkeep": 150_000
    },
    PlantType.HYDROPOWER: {
        "cost": 2_000_000,
        "output_mw": 60,
        "pollution_tco2e": 2,
        "location_constraints": "Requires proximity to rivers",
        "size": 25,
        "upkeep": 200_000
    },
    PlantType.NUCLEAR: {
        "cost": 4_000_000,
        "output_mw": 100,
        "pollution_tco2e": 50,
        "location_constraints": "Requires proximity to cooling water sources",
        "size": 20,
        "upkeep": 500_000
    }
}
