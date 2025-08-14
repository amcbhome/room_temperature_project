import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="IoT Temperature Simulator", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp", "temperature"])

# Function to simulate one temperature reading
def generate_temperature():
    base_temp = 22  # Average room temperature
    variation = np.random.normal(0, 0.5)  # Random fluctuation
    return round(base_temp + variation, 2)

st.title("IoT Room Temperature Simulator")

# Start/Stop buttons
col1, col2 = st.columns(2)
if col1.button("Start Simulation"):
    st.session_state.running = True
if col2.button("Stop Simulation"):
    st.session_state.running = False

# Main loop simulation
if "running" not in st.session_state:
    st.session_state.running = False

if st.session_state.running:
    # For demo purposes, generate data every second instead of every minute
    new_row = {
        "timestamp": datetime.now(),
        "temperature": generate_temperature()
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    time.sleep(1)
    st.experimental_rerun()

# Show latest reading
if not st.session_state.data.empty:
    latest_temp = st.session_state.data.iloc[-1]
    st.metric("Latest Temperature (°C)", latest_temp["temperature"], delta=None)

# Show data table
st.dataframe(st.session_state.data.tail(20))

# Show line chart
if not st.session_state.data.empty:
    st.line_chart(st.session_state.data.set_index("timestamp")["temperature"])

# Download option
csv = st.session_state.data.to_csv(index=False)
st.download_button("Download Data as CSV", data=csv, file_name="temperature_data.csv", mime="text/csv")
