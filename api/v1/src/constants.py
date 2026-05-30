SYSTEMS_TYPES = ["engine", "engine", "fuel", "navigation", "power_grid", "life_support", "thermal_control"]
SYSTEMS_STATUS = ["active", "warning", "failed"]
SENSORS = [
    {"name": "Main Engine Temperature", "unit": "celsius", "min_normal": 20, "max_normal": 850},
    {"name": "Fuel Tank Thermal Sensor", "unit": "celsius", "min_normal": -150, "max_normal": 30},
    {"name": "Reactor Core Cooling Sensor", "unit": "celsius", "min_normal": 50, "max_normal": 600},
    {"name": "Cabin Atmospheric Pressure", "unit": "atmosphere", "min_normal": 0.9, "max_normal": 1.1},
    {"name": "Fuel Pump Pressure", "unit": "bar", "min_normal": 10, "max_normal": 150},
    {"name": "Main Power Grid Voltage", "unit": "volt", "min_normal": 210, "max_normal": 230},
    {"name": "Solar Array Output", "unit": "watt", "min_normal": 0, "max_normal": 5000},
    {"name": "O2 Concentration Level", "unit": "percentage", "min_normal": 19, "max_normal": 23},
    {"name": "CO2 Scrubbers Saturation", "unit": "percentage", "min_normal": 0, "max_normal": 5},
    {"name": "Stabilization Gyroscope Speed", "unit": "rps", "min_normal": 100, "max_normal": 1500},
    {"name": "Hull G-Force Accelerometer", "unit": "g-force", "min_normal": 0, "max_normal": 6}
]
