import streamlit as st
import pickle
import numpy as np
import os
import pandas as pd
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Set page configuration
st.set_page_config(
    page_title="EV Range Estimator",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model - using absolute path to avoid directory navigation issues
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'ev_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)
    
# Load sample data for visualization
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ev_data.csv')
sample_data = pd.read_csv(data_path).sample(100)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #43a047;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #43a047;
    }
    .prediction-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1976d2;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    .reference-text {
        font-size: 0.8rem;
        color: #616161;
    }
</style>
""", unsafe_allow_html=True)

# App title with custom styling
st.markdown('<h1 class="main-header">🔋 EV Range Estimator</h1>', unsafe_allow_html=True)

# Create a nice dashboard layout with columns
st.markdown('<p class="info-box">This tool predicts the remaining range of an electric vehicle based on various sensor inputs using machine learning. Adjust the parameters below to see how different factors affect your EV\'s range.</p>', unsafe_allow_html=True)

# Sidebar for user input method selection
with st.sidebar:
    st.markdown('<h2 class="sub-header">⚙️ Settings</h2>', unsafe_allow_html=True)
    input_method = st.radio("Choose input method:", ["Sliders", "Direct Input"])
    show_advanced = st.checkbox("Show advanced visualizations")
    
    st.markdown("---")
    st.markdown('<h3 class="sub-header">📊 Reference Values</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    **Typical Ranges:**
    - **Battery Voltage:** 300-400V (Higher values typically indicate newer/higher-end EVs)
    - **Current:** 10-100A (Higher during acceleration, lower when cruising)
    - **Temperature:** 15-35°C (Optimal range; extremes reduce efficiency)
    - **State of Charge:** Best range prediction above 20%
    - **Speed:** Efficiency typically peaks at 50-70 km/h
    - **Load:** Additional weight reduces range (~1% per 50kg)
    """)
    
    # Add 3D model viewer (placeholder - would need a 3D model file)
    if st.checkbox("Show 3D EV Model"):
        st.markdown("3D Model would appear here with appropriate 3D library")

# Create a two-column layout for the main content
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<h2 class="sub-header">📝 Input Parameters</h2>', unsafe_allow_html=True)
    
    # Input fields - dynamically show sliders or number inputs based on user selection
    if input_method == "Sliders":
        battery_voltage = st.slider('Battery Voltage (V)', 300, 400, 360, help="Typical EV battery voltage ranges from 300V to 400V")
        current = st.slider('Current (A)', 10, 100, 45, help="Higher current = higher power consumption")
        temperature = st.slider('Battery Temperature (°C)', 0, 60, 30, help="Optimal temperature range is 15-35°C")
        soc = st.slider('State of Charge (%)', 0, 100, 75, help="Percentage of battery charge remaining")
        speed = st.slider('Vehicle Speed (km/h)', 0, 120, 50, help="Higher speeds reduce range due to air resistance")
        load = st.slider('Vehicle Load (kg)', 0, 500, 150, help="Additional weight beyond driver, passengers, and standard equipment")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            battery_voltage = st.number_input('Battery Voltage (V)', 300, 400, 360, help="Typical range: 300-400V")
            current = st.number_input('Current (A)', 10, 100, 45, help="Typical range: 10-100A")
            temperature = st.number_input('Battery Temperature (°C)', 0, 60, 30, help="Optimal: 15-35°C")
        with col_b:
            soc = st.number_input('State of Charge (%)', 0, 100, 75, help="Current battery level")
            speed = st.number_input('Vehicle Speed (km/h)', 0, 120, 50, help="Current speed")
            load = st.number_input('Vehicle Load (kg)', 0, 500, 150, help="Additional weight")

    predict_button = st.button("🚀 Predict Range", use_container_width=True)

with col2:
    if PLOTLY_AVAILABLE:
        # Create a gauge chart for the battery state of charge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = soc,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Battery State of Charge"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1E88E5"},
                'steps': [
                    {'range': [0, 20], 'color': "#EF5350"},
                    {'range': [20, 80], 'color': "#FFA726"},
                    {'range': [80, 100], 'color': "#66BB6A"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ))
        fig_gauge.update_layout(height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Add a temperature gauge
        temp_color = "#66BB6A" if 15 <= temperature <= 35 else "#EF5350"
        fig_temp = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = temperature,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Battery Temperature (°C)"},
            gauge = {
                'axis': {'range': [0, 60]},
                'bar': {'color': temp_color},
                'steps': [
                    {'range': [0, 15], 'color': "#90CAF9"},
                    {'range': [15, 35], 'color': "#66BB6A"},
                    {'range': [35, 60], 'color': "#EF5350"}
                ]
            }
        ))
        fig_temp.update_layout(height=250)
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        # Text-based alternatives if Plotly isn't available
        st.markdown(f"""
        ### Battery State of Charge: {soc}%
        {'🔴' if soc < 20 else '🟡' if soc < 80 else '🟢'} {'Low' if soc < 20 else 'Medium' if soc < 80 else 'High'}
        
        ### Battery Temperature: {temperature}°C
        {'❄️' if temperature < 15 else '✅' if temperature <= 35 else '🔥'} {'Cold' if temperature < 15 else 'Optimal' if temperature <= 35 else 'Hot'}
        """)
        
        # Simple progress bars
        st.text("SoC Level")
        st.progress(soc/100)
        
        st.text("Temperature (relative to optimal range)")
        # Normalize temperature to 0-1 scale where 0.5 is optimal
        temp_normalized = 1.0 - abs((temperature - 25) / 50)
        st.progress(temp_normalized)

# Prediction and visualization section
st.markdown("---")
if predict_button:
    # Create columns for prediction display and sensitivity analysis
    pred_col1, pred_col2 = st.columns([1, 2])
    
    with pred_col1:
        input_data = np.array([[battery_voltage, current, temperature, soc, speed, load]])
        prediction = model.predict(input_data)[0]
        st.markdown(
            f'<div class="prediction-box">'
            f'<h3>🔋 Estimated Range</h3>'
            f'<p style="font-size: 2.5rem; font-weight: bold; color: #1976d2;">{prediction:.2f} km</p>'
            f'<p>Based on the current parameters</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with pred_col2:
        if PLOTLY_AVAILABLE:
            # Create a radar chart comparing current input to optimal values
            categories = ['Voltage', 'Current', 'Temperature', 'SoC', 'Speed', 'Load']
            
            # Normalized values (0-1 scale)
            current_values = [
                (battery_voltage - 300) / 100,  # normalized to 0-1
                1 - (current - 10) / 90,        # lower current is better
                1 - abs((temperature - 25) / 35),  # optimal at 25°C
                soc / 100,                     # higher SoC is better
                1 - abs((speed - 60) / 60),    # optimal at ~60 km/h
                1 - (load / 500)               # lower load is better
            ]
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=current_values,
                theta=categories,
                fill='toself',
                name='Current Settings',
                line_color='#1E88E5'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                title="Parameter Efficiency (closer to edge is better)"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            # Text-based alternative showing parameter efficiency
            st.markdown("### Parameter Efficiency")
            st.markdown("Optimality of each parameter (100% = optimal):")
            
            efficiencies = [
                ("Battery Voltage", int((battery_voltage - 300) / 100 * 100)),
                ("Current Draw", int((1 - (current - 10) / 90) * 100)),
                ("Battery Temperature", int((1 - abs((temperature - 25) / 35)) * 100)),
                ("State of Charge", int(soc)),
                ("Speed", int((1 - abs((speed - 60) / 60)) * 100)),
                ("Vehicle Load", int((1 - (load / 500)) * 100))
            ]
            
            for param, efficiency in efficiencies:
                st.text(f"{param}: {efficiency}%")
                st.progress(efficiency/100)

# Advanced visualizations
if show_advanced:
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📊 Advanced Visualizations</h2>', unsafe_allow_html=True)
    
    if PLOTLY_AVAILABLE:
        # Display sample data visualization
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Create a scatter plot of SOC vs Range
            fig_scatter = px.scatter(
                sample_data, 
                x='soc', 
                y='physics_range',
                color='speed',
                size='load',
                hover_data=['battery_voltage', 'current', 'temperature'],
                title='State of Charge vs Range',
                labels={'soc': 'State of Charge (%)', 'physics_range': 'Range (km)'},
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col_viz2:
            # Create a 3D scatter plot
            fig_3d = px.scatter_3d(
                sample_data,
                x='soc',
                y='speed',
                z='physics_range',
                color='temperature',
                size='current',
                opacity=0.7,
                title='SOC, Speed, and Range Relationship',
                labels={'soc': 'State of Charge (%)', 'speed': 'Speed (km/h)', 'physics_range': 'Range (km)'}
            )
            fig_3d.update_layout(height=500)
            st.plotly_chart(fig_3d, use_container_width=True)
        
        # Create a heatmap showing the relationship between different variables
        st.markdown("### Correlation Heatmap")
        corr = sample_data[['battery_voltage', 'current', 'temperature', 'soc', 'speed', 'load', 'physics_range']].corr()
        fig_heatmap = px.imshow(
            corr, 
            text_auto=True, 
            aspect="auto", 
            color_continuous_scale=px.colors.sequential.Blues
        )
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("Advanced visualizations require Plotly. Install it with: pip install plotly")
        
        # Show a basic table with correlations
        st.markdown("### Key Relationships")
        st.markdown("""
        Based on the data, here are key relationships:
        
        - **State of Charge** has the strongest positive correlation with range
        - **Speed** has a moderate negative correlation with range at higher values
        - **Temperature** has an optimal range around 15-35°C
        - **Load** has a negative correlation with range - heavier vehicles travel less distance
        
        *Install Plotly to see interactive 3D visualizations and correlation heatmaps*
        """)
        
        # Display sample data in a table
        st.markdown("### Sample Data Preview")
        st.dataframe(sample_data.head(10))

# Footer with information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
<p>EV Range Estimator | Random Forest Model | © 2025</p>
<p class="reference-text">This tool uses a machine learning model trained on simulated electric vehicle data.</p>
</div>
""", unsafe_allow_html=True)
