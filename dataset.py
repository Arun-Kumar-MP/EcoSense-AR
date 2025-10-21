import pandas as pd
import numpy as np

np.random.seed(42)

def generate_environment_data(n=1000):
    data = []
    for _ in range(n):
        temp = np.random.uniform(15, 40)  # Temperature range
        humidity = np.random.uniform(25, 90)  # Humidity range
        air_index = np.random.uniform(0.5, 5.0)  # Rs/R0 ratio: 0.5 (polluted) to 5 (clean)
        lux = np.random.uniform(500, 50000)  # Light intensity
        
        # Rule-based label generation based on updated Air Index meaning
        if lux > 30000 and humidity < 50 and air_index > 3.6:
            plant = "Aloe Vera"        # Sun-loving, drought tolerant
        elif humidity > 70 and lux < 10000 and air_index > 2.0:
            plant = "Fern"             # Shade + humidity
        elif 20 < temp < 30 and 50 < humidity < 70 and 10000 < lux < 30000 and air_index > 2.5:
            plant = "Peace Lily"       # Medium light, medium humidity
        elif temp > 35 and humidity < 40 and air_index > 2.0:
            plant = "Cactus"           # Hot, dry
        elif air_index < 1.0 and humidity > 60:
            plant = "Money Plant"      # Tolerates pollution, humid
        elif lux < 5000:
            plant = "Spider Plant"     # Low light
        elif 5000 <= lux < 15000:
            plant = "Snake Plant"      # Medium light
        elif lux > 15000 and humidity > 55:
            plant = "Philodendron"     # Adaptable, thrives in moderate-high light
        elif lux > 20000 and temp > 28:
            plant = "Bougainvillea"    # Terrace, full sun
        elif 25 < temp < 35 and humidity > 60 and lux > 12000:
            plant = "Hibiscus"         # Flowering, terrace-friendly
        elif lux > 8000 and humidity > 50:
            plant = "Ivy"              # Vertical greening, walls
        elif lux > 10000 and air_index > 2.0:
            plant = "Bamboo"           # Pollution-tolerant, CO₂ absorber
        else:
            plant = "Philodendron"     # Default fallback

        data.append([round(temp, 2), round(humidity, 2), round(air_index, 2), round(lux, 2), plant])

    df = pd.DataFrame(data, columns=["Temperature", "Humidity", "Air_Index", "Lux", "Best_Plant"])
    return df

# Generate dataset
synthetic_df = generate_environment_data(1000)

# Save to CSV
synthetic_df.to_csv("Plant_Dataset.csv", index=False)

print(synthetic_df.head())
