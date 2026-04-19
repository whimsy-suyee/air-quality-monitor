import streamlit as st
from backend import fetch_aqi, get_aqi_status, get_health_advice
import matplotlib.pyplot as plt
import random

# 1. Page Layout
st.set_page_config(layout="wide")
st.title("🌍 Air Quality Monitor")
st.caption("Check real-time AQI and health recommendations")

# 2. Search Bar
col1, col2 = st.columns([4, 1])

with col1:
    city = st.text_input("Enter city name", label_visibility="collapsed")

with col2:
    search = st.button("Search")

st.divider()

# 3. Main
if search:
    with st.spinner("Fetching data..."):
        data = fetch_aqi(city)
    if not data:
        st.error("❌ City not found or API error")
    else:
        # Defining AQI
        aqi = data["aqi"]
        #  TOP SECTION 
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"📍 {data['city'].capitalize()}")

            if aqi is not None:
                st.metric("AQI", aqi)

                # STATUS + ADVICE
                status = get_aqi_status(aqi)
                advice = get_health_advice(aqi)

                st.success(status)

                st.markdown("### 💡 Health Recommendation")
                st.info(advice)

            else:
                st.warning("⚠️ AQI data temporarily unavailable")
                st.write("Try cities like: Bangkok, Singapore, Hanoi")

        # RIGHT SIDE (simple visual)
        with col2:
            st.markdown("### ")
            st.markdown("🟣")

        st.divider()

        # 4. TREND Graph for the past 7days 
        st.subheader("📈 AQI Trend (Last 7 Days)")

        if aqi is not None:
            trend_data = [aqi + random.randint(-20, 20) for _ in range(7)]

            fig, ax = plt.subplots()
            ax.plot(trend_data, marker='o')

            ax.set_title("AQI Trend")
            ax.set_xlabel("Days")
            ax.set_ylabel("AQI")

            ax.set_xticks(range(7))
            ax.set_xticklabels(["D1","D2","D3","D4","D5","D6","D7"])

            st.pyplot(fig)

        st.divider()

        st.subheader("Pollution Breakdown")

        pollutants = data["pollutants"]

        for name, value in pollutants.items():
            if value is not None:
                st.write(f"**{name.upper()}**: {value}")
                st.progress(min(float(value) / 200, 1.0))