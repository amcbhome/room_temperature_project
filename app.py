import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="IoT Room Temperature Simulator", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp", "temperature"])

if "running" not in st.session_state:
    st.session_state.running = False

# Function to simulate one temperature reading
def generate_temperature():
    base_temp = 22  # Average room temperature
    variation = np.random.normal(0, 0.5)  # Random fluctuation
    return round(base_temp + variation, 2)

st.title("IoT Room Temperature Simulator")

col1, col2 = st.columns(2)
if col1.button("Start Simulation"):
    st.session_state.running = True
if col2.button("Stop Simulation"):
    st.session_state.running = False

# Create placeholders for live updates
latest_placeholder = st.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Continuous streaming loop
while st.session_state.running:
    # Add a new reading
    new_row = {
        "timestamp": datetime.now(),
        "temperature": generate_temperature()
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )

    # Update UI in real-time
    latest_temp = st.session_state.data.iloc[-1]
    latest_placeholder.metric(
        "Latest Temperature (°C)",
        latest_temp["temperature"]
    )
    chart_placeholder.line_chart(
        st.session_state.data.set_index("timestamp")["temperature"]
    )
    table_placeholder.dataframe(st.session_state.data.tail(20))

    time.sleep(1)  # Wait 1 second before next reading

# Show static data when stopped
if not st.session_state.running and not st.session_state.data.empty:
    latest_temp = st.session_state.data.iloc[-1]
    st.metric("Latest Temperature (°C)", latest_temp["temperature"])
    st.line_chart(st.session_state.data.set_index("timestamp")["temperature"])
    st.dataframe(st.session_state.data.tail(20))

# Download option
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False)
    st.download_button("Download Data as CSV", data=csv, file_name="temperature_data.csv", mime="text/csv")

