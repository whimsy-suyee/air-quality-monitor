import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from backend import (
    fetch_aqi,
    fetch_multiple_cities,
    to_dataframe,
    get_aqi_status,
    get_health_advice,
)

st.set_page_config(
    page_title="Air Quality Monitor",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Air Quality Monitor Dashboard")
st.caption("Real-time AQI monitoring, pollutant breakdown, and health recommendations")

# Sidebar
st.sidebar.header("Settings")
default_cities = ["Phnom Penh", "Bangkok", "Hanoi", "Singapore", "Jakarta", "Delhi", "Hotan"]
selected_mode = st.sidebar.radio("Choose mode", ["Single City", "Compare Cities"])

st.sidebar.markdown("### Suggested Cities")
for c in default_cities:
    st.sidebar.write(f"- {c}")

# Header
st.divider()

if selected_mode == "Single City":
    col1, col2 = st.columns([5, 1])

    with col1:
        city = st.text_input("Enter city name", placeholder="e.g. Phnom Penh")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button("Search", use_container_width=True)

    if search:
        if not city.strip():
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Fetching AQI data..."):
                data = fetch_aqi(city)

            if not data:
                st.error("City not found or API error occurred.")
            else:
                aqi = data["aqi"]
                status = get_aqi_status(aqi)
                advice = get_health_advice(aqi)
                pollutants = data["pollutants"]

                top1, top2, top3 = st.columns(3)

                with top1:
                    st.metric("City", data["city"])
                with top2:
                    st.metric("AQI", aqi if aqi is not None else "N/A")
                with top3:
                    st.metric("Status", status)

                st.markdown("### 💡 Health Recommendation")
                st.info(advice)

                st.markdown("### 🧪 Pollutant Breakdown")
                pollutant_df = pd.DataFrame({
                    "Pollutant": list(pollutants.keys()),
                    "Value": list(pollutants.values())
                }).dropna()

                if not pollutant_df.empty:
                    fig, ax = plt.subplots()
                    ax.bar(pollutant_df["Pollutant"], pollutant_df["Value"])
                    ax.set_title("Pollutant Levels")
                    ax.set_xlabel("Pollutants")
                    ax.set_ylabel("Value")
                    st.pyplot(fig)

                    st.dataframe(pollutant_df, use_container_width=True)
                else:
                    st.warning("No pollutant data available.")

                st.markdown("### 📄 Raw AQI Details")
                detail_df = pd.DataFrame([{
                    "City": data["city"],
                    "AQI": aqi,
                    "Timestamp": data["timestamp"],
                    **pollutants
                }])
                st.dataframe(detail_df, use_container_width=True)

                csv = detail_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download AQI Data as CSV",
                    data=csv,
                    file_name="aqi_data.csv",
                    mime="text/csv"
                )

elif selected_mode == "Compare Cities":
    city_input = st.text_area(
        "Enter multiple cities separated by commas",
        placeholder="Phnom Penh, Bangkok, Hanoi, Singapore"
    )

    compare = st.button("Compare")

    if compare:
        cities = [c.strip() for c in city_input.split(",") if c.strip()]

        if not cities:
            st.warning("Please enter at least one city.")
        else:
            with st.spinner("Fetching AQI data for multiple cities..."):
                results = fetch_multiple_cities(cities)

            if not results:
                st.error("No valid city data found.")
            else:
                df = to_dataframe(results)

                st.markdown("### 📊 City Comparison Table")
                st.dataframe(df, use_container_width=True)

                valid_df = df.dropna(subset=["AQI"])

                if not valid_df.empty:
                    st.markdown("### 📈 AQI Comparison Chart")
                    fig, ax = plt.subplots()
                    ax.bar(valid_df["City"], valid_df["AQI"])
                    ax.set_title("AQI by City")
                    ax.set_xlabel("City")
                    ax.set_ylabel("AQI")
                    plt.xticks(rotation=30)
                    st.pyplot(fig)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Comparison Data as CSV",
                    data=csv,
                    file_name="aqi_comparison.csv",
                    mime="text/csv"
                )
