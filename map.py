import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
import io
import base64
import re


def normalize_text(s):
    if not isinstance(s, str):
        return s
    s = s.lower().strip()
    s = s.replace("&", "and").replace(" ", "")
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


master_df = pd.read_parquet("data/processed/master_dataset.parquet")
detect_surgeons = pd.read_csv("data/processed/detected_surges.csv")
districts_gdf_0 = gpd.read_file("data/external/INDIA_DISTRICTS_0.geojson")
districts_gdf_1 = gpd.read_file("data/external/INDIA_DISTRICTS_1.geojson")
districts_gdf = gpd.GeoDataFrame(
    pd.concat([districts_gdf_0, districts_gdf_1], ignore_index=True),
    crs=districts_gdf_0.crs
)


detect_surgeons['surge_multiplier'] = (detect_surgeons['surge_multiplier'] - detect_surgeons['surge_multiplier'].min())/(detect_surgeons['surge_multiplier'].max() - detect_surgeons['surge_multiplier'].min())
detect_surgeons['total_updates'] = (detect_surgeons['total_updates'] - detect_surgeons['total_updates'].min())/(detect_surgeons['total_updates'].max() - detect_surgeons['total_updates'].min())

master_df["state"] = master_df["state"].apply(normalize_text)
master_df["district"] = master_df["district"].apply(normalize_text)
districts_gdf["state"] = districts_gdf["state"].apply(normalize_text)
districts_gdf["district"] = districts_gdf["district"].apply(normalize_text)
detect_surgeons['state'] = detect_surgeons['state'].apply(normalize_text)


def create_pie_chart_marker(lat, lon, bio_child, bio_adult, state_name, m):
    if bio_child == 0 and bio_adult == 0:
        return

    sizes = [bio_child, bio_adult]
    colors = ["#ff9999", "#66b3ff"]

    fig, ax = plt.subplots(figsize=(1.5, 1.5))
    ax.pie(sizes, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    img_data = io.BytesIO()
    plt.savefig(
        img_data, format="png", transparent=True, bbox_inches="tight", pad_inches=0.1
    )
    plt.close(fig)

    encoded_img = base64.b64encode(img_data.getvalue()).decode("utf-8")

    icon = folium.features.CustomIcon(
        icon_image=f"data:image/png;base64,{encoded_img}",
        icon_size=(100, 100),
        icon_anchor=(50, 50),
    )

    folium.Marker(
        location=[lat, lon],
        icon=icon,
        popup=f"{state_name}<br>Age: 5-17: {bio_child}<br>Age: 18+: {bio_adult}",
    ).add_to(m)


def add_legend(m,a='child',b='adult',leg = "legend"):
    legend_html = f"""
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white;
     ">
     &nbsp; <b>{leg}</b> <br>
     &nbsp; <i class="fa fa-circle" style="color:#ff9999"></i> &nbsp; {a} <br>
     &nbsp; <i class="fa fa-circle" style="color:#66b3ff"></i> &nbsp; {b} <br>
      </div>
     """
    m.get_root().html.add_child(folium.Element(legend_html))


def main_sugeons():
    state_summary = (
        detect_surgeons.groupby("state")[["total_updates", "surge_multiplier"]]
        .sum()
        .reset_index()
    )

    districts_gdf["geometry"] = districts_gdf.geometry.buffer(0)
    states_gdf = districts_gdf.dissolve(
        by="state", aggfunc="sum"
    ).reset_index()

    merged_gdf = states_gdf.merge(state_summary, on="state", how="left")

    merged_gdf[["total_updates", "surge_multiplier"]] = merged_gdf[
        ["total_updates", "surge_multiplier"]
    ].fillna(0)

    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    marker_cluster = MarkerCluster().add_to(india_map)

    for _, row in merged_gdf.iterrows():
        centroid = row.geometry.centroid
        lat, lon = centroid.y, centroid.x

        create_pie_chart_marker(
            lat,
            lon,
            row["total_updates"],
            row["surge_multiplier"],
            row["state"],
            marker_cluster,
        )

    add_legend(india_map, "total_updates","surge_multiplier", "peak time Adhaar activity")

    india_map.save("outputs/maps/surgeons_state_pie_chart_map.html")
    print("Map saved to surgeons_state_pie_chart_map.html")


def main_district():
    state_summary = (
        master_df.groupby(["state", "district"])[["bio_child", "bio_adult"]]
        .sum()
        .reset_index()
    )

    districts_gdf["geometry"] = districts_gdf.geometry.buffer(0)
    states_gdf = districts_gdf.dissolve(
        by=["state", "district"], aggfunc="sum"
    ).reset_index()

    merged_gdf = states_gdf.merge(state_summary, on=["state", "district"], how="left")

    merged_gdf[["bio_child", "bio_adult"]] = merged_gdf[
        ["bio_child", "bio_adult"]
    ].fillna(0)

    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    marker_cluster = MarkerCluster().add_to(india_map)

    for _, row in merged_gdf.iterrows():
        centroid = row.geometry.centroid
        lat, lon = centroid.y, centroid.x

        create_pie_chart_marker(
            lat,
            lon,
            row["bio_child"],
            row["bio_adult"],
            row["district"],
            marker_cluster,
        )

    add_legend(india_map,leg="District-wise Biometric updation")

    india_map.save("outputs/maps/district_biometric_pie_chart_map.html")
    print("Map saved to district_biometric_pie_chart_map.html")


def main_state():
    state_summary = (
        master_df.groupby("state")[["bio_child", "bio_adult"]].sum().reset_index()
    )

    districts_gdf["geometry"] = districts_gdf.geometry.buffer(0)
    states_gdf = districts_gdf.dissolve(by="state", aggfunc="sum").reset_index()

    merged_gdf = states_gdf.merge(state_summary, on="state", how="left")

    merged_gdf[["bio_child", "bio_adult"]] = merged_gdf[
        ["bio_child", "bio_adult"]
    ].fillna(0)

    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    marker_cluster = MarkerCluster().add_to(india_map)

    for _, row in merged_gdf.iterrows():
        centroid = row.geometry.centroid
        lat, lon = centroid.y, centroid.x

        create_pie_chart_marker(
            lat, lon, row["bio_child"], row["bio_adult"], row["state"], marker_cluster
        )

    add_legend(india_map,leg="State-wise Biometric Updation")

    india_map.save("outputs/maps/state_biometric_pie_chart_map.html")
    print("Map saved to state_biometric_pie_chart_map.html")


if __name__ == "__main__":
    main_district()
    main_state()
    main_sugeons()