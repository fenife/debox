import streamlit as st
import pandas as pd
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium

def main():
    # 设置页面标题
    st.title('经纬度轨迹地图绘制')
    st.write('上传包含经纬度的CSV文件或直接输入经纬度数据，绘制轨迹路线')
    
    # 数据输入方式选择
    input_method = st.radio("选择数据输入方式：", ("上传CSV文件", "手动输入经纬度"), index=1)
    
    # 初始化数据
    df = None
    
    if input_method == "上传CSV文件":
        # 文件上传
        uploaded_file = st.file_uploader("选择包含经纬度的CSV文件", type="csv")
        
        if uploaded_file is not None:
            # 读取CSV文件
            df = pd.read_csv(uploaded_file)
            
            # 检查是否包含必要的列
            required_columns = ['latitude', 'longitude']
            if not all(col in df.columns for col in required_columns):
                st.error("CSV文件必须包含 'latitude' (纬度) 和 'longitude' (经度) 列")
            else:
                st.success("文件上传成功！")
                st.subheader("数据预览")
                st.dataframe(df.head())
    
    else:  # 手动输入经纬度
        st.write("请输入经纬度数据，格式为：纬度,经度，每行一个点")
        st.write("示例：")
        st.code("39.9042,116.4074\n38.0500,114.5149\n37.8716,112.5623")
        
        # 文本区域输入
        coords_text = st.text_area("输入经纬度数据", height=200)
        
        if coords_text:
            # 解析输入
            coords_list = []
            lines = coords_text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        lat, lon = map(float, line.split(','))
                        coords_list.append((lat, lon))
                    except ValueError:
                        st.warning(f"无法解析行: {line}，请检查格式")
            
            if coords_list:
                # 创建DataFrame
                df = pd.DataFrame(coords_list, columns=['latitude', 'longitude'])
                st.success(f"成功解析 {len(coords_list)} 个坐标点")
                st.subheader("数据预览")
                st.dataframe(df)
    
    # 绘制地图
    if df is not None and not df.empty:
        st.subheader("轨迹地图")
        
        # 计算中心点
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        
        # 创建地图
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        
        # 添加轨迹
        points = df[['latitude', 'longitude']].values.tolist()
        
        # 添加带动画效果的轨迹线
        AntPath(
            points,
            color="blue",
            weight=5,
            opacity=0.6,
            dash_array="10, 20",
            delay=1000,
            pulse_color="#3186cc"
        ).add_to(m)
        
        # 添加起点和终点标记
        if len(points) > 0:
            # 起点
            folium.Marker(
                location=points[0],
                popup="起点",
                icon=folium.Icon(color="green", icon="flag")
            ).add_to(m)
            
            # 终点
            folium.Marker(
                location=points[-1],
                popup="终点",
                icon=folium.Icon(color="red", icon="flag")
            ).add_to(m)
        
        # 在Streamlit中显示地图
        st_folium(m, width=1500, height=1000)
        
        # # 提供数据下载选项
        # csv = df.to_csv(index=False)
        # st.download_button(
        #     label="下载数据为CSV",
        #     data=csv,
        #     file_name="coordinates.csv",
        #     mime="text/csv",
        # )

if __name__ == "__main__":
    main()
