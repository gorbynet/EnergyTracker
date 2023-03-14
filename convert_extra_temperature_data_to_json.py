# The weather API I initialled used was missing data from 2023-01-02 to 2023-01-23
# I found a secondary data source, https://www.timeanddate.com/weather/
# This is parsing the JSON data embedded in that 
# page to extract temperatures for the missing dates and aligning them to the hourly 
# schedule as the original data source

import pandas as pd
import json
import datetime as dt
import os
from Utils import extra_data as ed

jan_data=json.loads(ed)

extra_temp_df = (pd.DataFrame(jan_data['temp'])
    .assign(date = lambda row: pd.to_datetime(row['date'], unit='ms', utc=True) - dt.timedelta(minutes=20))
    .rename({'temp': 'temperature'}, axis=1)
    .set_index('date')
).loc['2023-01-02':'2023-01-23'].resample('H').mean()
extra_temp_df.to_csv(os.path.join('Data', '2023-01-02_2023_01_23_weather.csv'), index=True)
