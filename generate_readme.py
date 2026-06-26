import json
import sys
from datetime import datetime, timezone, timedelta

wib = timezone(timedelta(hours=7))

def get_wind_dir(deg):
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[round(deg / 45) % 8]

def unix_to_wib(ts):
    return datetime.fromtimestamp(ts, tz=wib).strftime("%H:%M")

# Load weather
with open("weather.json") as f:
    w = json.load(f)

# Load air quality
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

aqi_labels = {1:"Good", 2:"Fair", 3:"Moderate", 4:"Poor", 5:"Very Poor"}
aqi_colors = {1:"#22c55e", 2:"#84cc16", 3:"#f59e0b", 4:"#ef4444", 5:"#dc2626"}
aqi_emojis = {1:"🟢", 2:"🟡", 3:"🟠", 4:"🔴", 5:"🟣"}

aqi_label = aqi_labels.get(aqi_num, "Unknown") if aqi_num else "Unknown"
aqi_color = aqi_colors.get(aqi_num, "#888888") if aqi_num else "#888888"
aqi_emoji = aqi_emojis.get(aqi_num, "") if aqi_num else ""

def card(label, value, sub="", value_color="#e2e8f0"):
    sub_html = f'<p style="margin:2px 0 0;font-size:11px;color:#64748b;">{sub}</p>' if sub else ""
    return f"""    <td style="padding:6px;">
      <div style="background:#1e293b;border-radius:10px;padding:10px 12px;min-width:120px;">
        <p style="margin:0 0 4px;font-size:11px;color:#64748b;">{label}</p>
        <p style="margin:0;font-size:15px;font-weight:600;color:{value_color};">{value}</p>
        {sub_html}
      </div>
    </td>"""

readme = f"""# 🌦️ Jakarta Weather Tracker

> Cuaca Jakarta diperbarui otomatis via [OpenWeatherMap](https://openweathermap.org/) · Update: 07:00 – 22:00 WIB

<div align="center">

![Jakarta Weather](./card.svg)

</div>

---

## 📊 {condition} — {day_name}

<div align="center">
<table style="border-collapse:collapse;background:#0f172a;border-radius:16px;overflow:hidden;">
  <tr>
{card("🌡️ Suhu", f"{temp}°C", f"terasa {feels}°C")}
{card("🌡️ Min / Max", f"{temp_min}° / {temp_max}°", "hari ini")}
{card("💧 Kelembapan", f"{humidity}%")}
  </tr>
  <tr>
{card("🌬️ Angin", f"{wind_speed} m/s", f"dari {wind_dir}")}
{card("☁️ Tutupan Awan", f"{clouds}%")}
{card("👁️ Jarak Pandang", f"{visibility} km")}
  </tr>
  <tr>
{card("🌫️ Tekanan", f"{pressure} hPa")}
{card("🌧️ Hujan (1 jam)", rain_str)}
{card("🏭 Kualitas Udara", f"{aqi_label} {aqi_emoji}", f"AQI {aqi_num}" if aqi_num else "", value_color=aqi_color)}
  </tr>
  <tr>
{card("🌅 Matahari Terbit", sunrise, "WIB")}
{card("🌇 Matahari Terbenam", sunset, "WIB")}
{card("🕗 Diperbarui", updated, "")}
  </tr>
</table>
</div>

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
