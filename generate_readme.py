import json
from datetime import datetime, timezone, timedelta

wib = timezone(timedelta(hours=7))

def get_wind_dir(deg):
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[round(deg / 45) % 8]

def unix_to_wib(ts):
    return datetime.fromtimestamp(ts, tz=wib).strftime("%H:%M")

with open("weather.json") as f:
    w = json.load(f)

try:
    with open("air.json") as f:
        a = json.load(f)
    aqi_num = a["list"][0]["main"]["aqi"]
except:
    aqi_num = None

temp      = round(w["main"]["temp"])
feels     = round(w["main"]["feels_like"])
temp_min  = round(w["main"]["temp_min"])
temp_max  = round(w["main"]["temp_max"])
humidity  = w["main"]["humidity"]
pressure  = w["main"]["pressure"]
wind_speed= w["wind"]["speed"]
wind_dir  = get_wind_dir(w["wind"].get("deg", 0))
clouds    = w["clouds"]["all"]
visibility= round(w.get("visibility", 0) / 1000, 1)
condition = w["weather"][0]["description"].title()
rain_1h   = w.get("rain", {}).get("1h", None)
rain_str  = f"{rain_1h} mm" if rain_1h else "—"
sunrise   = unix_to_wib(w["sys"]["sunrise"])
sunset    = unix_to_wib(w["sys"]["sunset"])

updated   = datetime.now(tz=wib).strftime("%d %B %Y, %H:%M WIB")
day_name  = datetime.now(tz=wib).strftime("%A, %d %B %Y")

aqi_labels = {1:"Good 🟢", 2:"Fair 🟡", 3:"Moderate 🟠", 4:"Poor 🔴", 5:"Very Poor 🟣"}
aqi_label  = aqi_labels.get(aqi_num, "Unknown") if aqi_num else "Unknown"
aqi_str    = f"{aqi_label} (AQI {aqi_num})" if aqi_num else "—"

readme = f"""# 🌦️ Jakarta Weather Tracker

> Cuaca Jakarta diperbarui otomatis via [OpenWeatherMap](https://openweathermap.org/) · Update: 07:00 – 22:00 WIB

<div align="center">

![Jakarta Weather](./card.svg)

</div>

---

## 📊 {condition} — {day_name}

| | | | |
|:---:|:---|:---:|:---|
| 🌡️ | **Suhu** &nbsp; `{temp}°C` *(terasa {feels}°C)* | 💧 | **Kelembapan** &nbsp; `{humidity}%` |
| 🌡️ | **Min / Max** &nbsp; `{temp_min}° / {temp_max}°` | ☁️ | **Tutupan Awan** &nbsp; `{clouds}%` |
| 🌬️ | **Angin** &nbsp; `{wind_speed} m/s` dari `{wind_dir}` | 👁️ | **Jarak Pandang** &nbsp; `{visibility} km` |
| 🌫️ | **Tekanan** &nbsp; `{pressure} hPa` | 🌧️ | **Hujan (1 jam)** &nbsp; `{rain_str}` |
| 🌅 | **Sunrise** &nbsp; `{sunrise} WIB` | 🌇 | **Sunset** &nbsp; `{sunset} WIB` |
| 🏭 | **Kualitas Udara** &nbsp; {aqi_str} | 🕗 | **Update** &nbsp; `{updated}` |

---

## 📂 Data & Log

| File | Deskripsi |
|:---|:---|
| 📄 [weather.json](./weather.json) | Raw data cuaca terbaru dari API |
| 🎨 [card.svg](./card.svg) | Weather card (SVG) |
| 📁 [history/](./history) | Snapshot cuaca per sesi |

---

<sub>⚙️ Dijalankan otomatis oleh [GitHub Actions](../../actions) · Sumber: OpenWeatherMap API</sub>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README.md generated successfully")
