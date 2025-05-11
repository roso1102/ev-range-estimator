import numpy as np
import pandas as pd
import os

def generate_ev_data(n_samples=1000, random_state=42):
    np.random.seed(random_state)

    battery_voltage = np.random.normal(360, 15, n_samples).clip(300, 400)
    current = np.random.normal(40, 10, n_samples).clip(10, 100)
    temperature = np.random.normal(25, 8, n_samples).clip(-10, 60)
    soc = np.random.uniform(10, 100, n_samples)
    speed = np.random.normal(60, 20, n_samples).clip(0, 120)
    load = np.random.normal(150, 60, n_samples).clip(50, 500)

    energy_wh = battery_voltage * soc / 100 * 85
    efficiency_wh_per_km = (current * speed * 0.1 + load * 0.05 + np.abs(temperature - 25) * 2).clip(100, 300)
    physics_range = (energy_wh / efficiency_wh_per_km).clip(0, 600)

    ml_range = (
        soc * 2.5 - current * 0.8 - speed * 0.4
        - load * 0.05 - np.abs(temperature - 25) * 1.8
        + np.random.normal(0, 15, n_samples)
    ).clip(0, 600)

    df = pd.DataFrame({
        "battery_voltage": battery_voltage.round(2),
        "current": current.round(2),
        "temperature": temperature.round(2),
        "soc": soc.round(2),
        "speed": speed.round(2),
        "load": load.round(2),
        "physics_range": physics_range.round(2),
        "ml_range": ml_range.round(2)
    })

    # Save to data/ev_data.csv
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/ev_data.csv", index=False)
    print("✅ Data saved to data/ev_data.csv")

if __name__ == "__main__":
    generate_ev_data()
