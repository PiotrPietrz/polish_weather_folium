import requests
import json
import pandas as pd
import re


class Connector:
    def get_data(self, url: str) -> pd.DataFrame:
        r = requests.get(url)
        response = json.loads(r.text)

        df = pd.json_normalize(response)

        return df

    def get_result(self, url: str, city: str) -> pd.DataFrame:

        d = self.get_data(url)

        l = list(
            filter(lambda x: re.match("properties.parameter.T2M*", x), list(d.columns))
        )
        params = d[l[:-1]]
        params = params.rename(
            columns={column: column[-6:] for column in params.columns.tolist()}
        )
        params = params.T.reset_index().rename(
            columns={"index": "month", 0: "temperature"}
        )
        params["city"] = city

        return params

    def fetch(
        self, lats: pd.Series, lons: pd.Series, cities: pd.Series
    ) -> pd.DataFrame:
        dfs = []

        # fetching data for all of the points
        for lat, lon, cty in zip(lats, lons, cities):
            url = f"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=T2M&community=RE&longitude={lon}&latitude={lat}&format=JSON&start=2021&end=2021&user=DAV"

            print(f"Fetching for {cty}...")
            d = self.get_result(url=url, city=cty)

            dfs.append(d)

        print("Concatenating the results...")
        res = pd.concat(dfs)
        res = res.reset_index(drop=True)

        print("Saving backup...")
        res.to_parquet("params.parquet")

        return res
