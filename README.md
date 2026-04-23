# air-quality-monitor
COSC 121 Final Project
---

## 📦 Requirements

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI |
| `requests` | API calls |
| `pandas` | Data table |

Install all at once:
```bash
pip install streamlit requests pandas
```

---

## 🔑 API Token

This project uses the [World Air Quality Index API](https://aqicn.org/data-platform/token/).

1. Get a free token at https://aqicn.org/data-platform/token/
2. Open `aqi_monitor.py`
3. Replace the token value:
```python
API_TOKEN = "your_token_here"
```

---

## 🏥 AQI Scale

| Range | Status |
|-------|--------|
| 0–50 | Good 🟢 |
| 51–100 | Moderate 🟡 |
| 101–150 | Unhealthy for Sensitive Groups 🟠 |
| 151–200 | Unhealthy 🔴 |
| 201–300 | Very Unhealthy 🟣 |
| 300+ | Hazardous ⚫ |

---

## 📡 Data Source
[World Air Quality Index Project][(https://aqicn.org/data-platform/token/)]
