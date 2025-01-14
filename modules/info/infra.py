from enum import Enum


class InfraType(Enum):
    BATTERY_ENERGY_GRID_STORAGE = "battery energy grid storage",
    PUMPED_HYDROELECTRIC_ENERGY_STORAGE = "pumped hydroelectric energy storage",
    MAINTENANCE_CENTER = "maintenance center",


storage = (InfraType.BATTERY_ENERGY_GRID_STORAGE, InfraType.PUMPED_HYDROELECTRIC_ENERGY_STORAGE)

infra = {
    InfraType.BATTERY_ENERGY_GRID_STORAGE: {
        "cost": 1_000_000,
        "capacity_mw": 50,
        "upkeep": 100_000,
        "description": "Stores surplus energy and releases it during shortages to stabilize the grid.",
        "size": (5, 5)
    },
    InfraType.PUMPED_HYDROELECTRIC_ENERGY_STORAGE: {
        "cost": 3_000_000,
        "capacity_mw": 300,
        "upkeep": 250_000,
        "description": "Uses excess energy to pump water uphill "
                       "and releases it to generate power during demand spikes.",
        "size": (15, 15)
    },
    InfraType.MAINTENANCE_CENTER: {
        "cost": 500_000,
        "radius": 10,
        "upkeep_reduction": 0.2,
        "upkeep": 50_000,
        "description": "Reduces maintenance costs and increases the lifespan of nearby infrastructure.",
        "size": (5, 5),
        'asset_id': 'maintenance'
    }
}
