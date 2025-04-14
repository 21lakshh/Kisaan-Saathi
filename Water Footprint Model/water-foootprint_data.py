import pandas as pd
import random

# Define possible values
crops = ["Wheat", "Rice", "Maize", "Sugarcane", "Cotton"]
regions = ["Punjab", "Maharashtra", "UP", "Karnataka", "Bihar"]
soils = ["Loamy", "Sandy", "Clayey"]
methods = ["Drip", "Sprinkler", "Flood"]

# Create a synthetic dataset
data = []
for _ in range(500):  # You can change this to generate more rows
    crop = random.choice(crops)
    region = random.choice(regions)
    soil = random.choice(soils)
    irrigation = random.choice(methods)
    
    # Generate climate values based on crop and region logic
    rainfall = random.randint(200, 1200)  # mm
    temperature = random.randint(18, 38)  # °C
    humidity = random.randint(30, 90)     # %

    # Water footprint logic (simplified)
    base_fp = {
        "Wheat": 1300,
        "Rice": 2500,
        "Maize": 1200,
        "Sugarcane": 3500,
        "Cotton": 2200
    }[crop]
    
    modifier = 1
    if irrigation == "Drip":
        modifier -= 0.15
    elif irrigation == "Sprinkler":
        modifier -= 0.1
    if soil == "Sandy":
        modifier += 0.1
    if rainfall > 900:
        modifier -= 0.1
    elif rainfall < 400:
        modifier += 0.1
    
    footprint = int(base_fp * modifier + random.uniform(-100, 100))  # Add noise

    data.append([crop, region, soil, irrigation, rainfall, temperature, humidity, footprint])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "CropType", "Region", "SoilType", "IrrigationMethod",
    "Rainfall", "Temperature", "Humidity", "WaterFootprint"
])

# Save as CSV
df.to_csv("Water Footprint Model/crop_water_data.csv", index=False)
print("✅ Synthetic dataset saved as crop_water_data.csv")
