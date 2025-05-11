# EV Range Estimator 🔋🚗

A machine learning project that predicts the remaining range of an electric vehicle based on sensor inputs.

## Features
- Regression model (Random Forest)
- Interactive Streamlit app with advanced visualizations
- Direct input and slider options for parameters
- Gauges and efficiency metrics
- 3D visualization of relationships between variables
- Input: Battery voltage, current, temperature, SOC, speed, load
- Output: Estimated range in km

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For enhanced visualizations, install Plotly:
```bash
pip install plotly
```

## Usage
1. Generate sample data (if not already present):
```bash
python src/simulate_ev_range_data.py
```

2. Train the model:
```bash
python model/train_model.py
```

3. Run the interactive app:
```bash
streamlit run app/app.py
```

## Interactive Features
- Choose between slider controls or direct numeric input
- Real-time prediction of EV range
- Visual battery and temperature gauges
- Parameter efficiency visualization
- Advanced 3D relationship plots and correlation heatmaps
- Reference values and optimal ranges

## Screenshots
(Screenshots of the app would be displayed here)
```bash
python model/train_model.py
