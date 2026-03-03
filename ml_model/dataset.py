import pandas as pd
import numpy as np

np.random.seed(42)

def generate_environment_data(n=2000):
    data = []
    for _ in range(n):
        temp = np.random.uniform(15, 40)
        humidity = np.random.uniform(25, 90)
        air_index = np.random.uniform(0.5, 5.0)
        
        selector = np.random.rand()
        
        if selector < 0.2: # 20% of data is "Covered"
            lux = np.random.uniform(0, 9)
            plant = "Money Plant"
        elif selector < 0.5: # 30% of data is "Normal Room"
            lux = np.random.uniform(10, 500)
            plant = "Monstera Deliciosa"
        elif selector < 0.6: # 10% Transition
            lux = np.random.uniform(501, 15000)
            plant = "Philodendron"
        elif selector < 0.7: # 10% Transition
            lux = np.random.uniform(15001, 35000)
            plant = "Snake Plant"
        else: # 30% of data is "Torch Light"
            lux = np.random.uniform(35001, 50000)
            plant = "Aloe Vera"
            
        data.append([round(temp, 2), round(humidity, 2), round(air_index, 2), round(lux, 2), plant])

    df = pd.DataFrame(data, columns=["Temperature", "Humidity", "Air_Index", "Lux", "Best_Plant"])
    return df

# Save and overwrite
synthetic_df = generate_environment_data(2000)
synthetic_df.to_csv("Plant_Dataset.csv", index=False)

print("Successfully Created!")
print(synthetic_df['Best_Plant'].value_counts())