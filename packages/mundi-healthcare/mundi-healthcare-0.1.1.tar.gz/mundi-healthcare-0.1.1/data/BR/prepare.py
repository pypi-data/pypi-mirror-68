#
# DATA EXTRACTED FROM CNES
#
from pathlib import Path

import mundi
import pandas as pd

PATH = Path(__file__).parent.resolve()
DEST = PATH / 'processed'

cities = mundi.regions(country_code="BR", type="city")
cities = (
    cities.mundi['short_code']
        .reset_index()
        .rename({'short_code': 'city_id'}, axis=1)
)

data = pd.read_csv(PATH / 'cnes_2020-02.csv', dtype={'city_id': 'string'})
data = (
    data[["city_id", "clinical", "clinical_sus", "icu", "icu_sus"]]
        .set_index("city_id")
        .groupby("city_id")
        .sum()
        .reset_index()
)

data = (
    pd.merge(cities, data, on='city_id')
        .drop(columns='city_id')
        .set_index('id')
        .rename({
        'clinical': 'hospital_capacity',
        'clinical_sus': 'hospital_capacity_public',
        'icu': 'icu_capacity',
        'icu_sus': 'icu_capacity_public',
    }, axis=1)
)

data.to_pickle(DEST / 'capacity-C1.pkl')
print("Data saved!")
