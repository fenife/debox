from streamlit_folium import st_folium
import folium
m = folium.Map(location=[39.9042, 116.4074], zoom_start=10)
# 添加轨迹线（经纬度列表）
folium.PolyLine(
    locations=[(39.9, 116.4), (39.8, 116.5), (39.7, 116.6)],
    color="blue", weight=2.5, opacity=1
).add_to(m)
# m.save("trace_map.html")  # 保存为HTML

st_folium(m)
