import folium
import json
import altair as alt
import pandas as pd


class DraftMap:
    def draft_map(self, lat: pd.Series, lon: pd.Series) -> folium.Map:
        m = folium.Map(location=[lat.mean(), lon.mean()], zoom_start=7)

        for lat, lon in zip(lat, lon):
            folium.Marker(location=[lat, lon]).add_to(m)

        return m


class FinalMap:
    def final_map(
        self, base_df: pd.DataFrame, temperature_df: pd.DataFrame
    ) -> folium.Map:

        m = folium.Map(
            location=[base_df["lat"].mean(), base_df["lng"].mean()], zoom_start=7
        )

        for city in temperature_df.city.unique():

            # base df for the visual
            base = base_df[base_df.city == city].reset_index()
            lat = base.at[0, "lat"]
            lon = base.at[0, "lng"]

            d = temperature_df[temperature_df.city == city]

            # creating a chart
            chart = (
                alt.Chart(data=d, height=150, width=400, title=city)
                .mark_line()
                .encode(x="month", y="temperature")
            )

            popup = folium.Popup()
            folium.features.VegaLite(chart.to_json(), height=150, width=450).add_to(
                popup
            )
            folium.Marker(location=[lat, lon], popup=popup).add_to(m)

        return m
