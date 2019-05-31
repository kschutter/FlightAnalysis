import numpy as np
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
import os
plt.style.use('ggplot')

''' Schema:
        `adshex` Unique identifier for each aircraft.
        `flight_id` Unique identifier for each "flight segment."
        `latitude`, `longitude` Geographic location in digital degrees.
        `altitude` Altitude in feet.
        `speed` Ground speed in knots.
        `track` Compass bearing in degrees, with 0 corresponding to north.
        `squawk` Four-digit code transmitted by the transponder.
        `type` Aircraft model, if identified.
        `timestamp` Full UTC timestamp.
        `name` Name of aircraft registrant.
        `other_names1`, `other_names2` Other names for the registrant, if listed.
        `n_number` Aircraft registration number.
        `serial_number` Identifying number assigned to the aircraft by its manufacturer.
        `mfr_mdl_code` Code designating the manufacturer and model of the aircraft.
        `mfr` Manufacturer.
        `model` Aircraft model.
        `year_mfr` Year in which aircraft was manufactured.
        `type_aircraft` `4`: fixed-wing single-engine, `5`: fixed-wing multi-engine, `6`: helicopter.
        `agency` Federal agency operating the aircraft.
'''

df = pd.read_csv('../data/fulldata')

# def get_list_of_days:
day_query = '''
            SELECT
                DATE(timestamp) as DateField
            FROM df
            GROUP BY DATE(timestamp)
            '''
days = ps.sqldf(day_query, locals()).values

for day in days:
    groupby_days = f'''
                    SELECT *
                    FROM df
                    WHERE DATE(timestamp) = '{day[0]}'
                    '''
    chunk = ps.sqldf(groupby_days, locals())
    chunk.to_csv(f'../data/days/{day[0]}.csv')
    print(f"saved {day[0]}.csv")

df_flight_paths = ps.sqldf(agg_into_list, locals())
df_flight_paths.to_csv('../data/pinlist.csv')

duration = .5  # seconds
freq = 440  # Hz
os.system(f'play -nq -t alsa synth {duration} sine {freq}')

# Remove less interesting columns
def reduce(df):
    bad_data = ['squawk','type', 'other_names1', 'other_names2', 'mfr_mdl_code',
                'serial_number', 'year_mfr', 'type_aircraft']
    for name in bad_data:
        df.drop(name, axis=1, inplace=True)

# Create two column df of flight ids and tuple of that location
def makeCSVofpins():
    flight_query = '''
                    SELECT
                        flight_id,
                        longitude,
                        latitude
                    FROM df
                    '''
    df_flight_paths = ps.sqldf(flight_query, locals())
    df_flight_paths['pins'] = [ tuple(row[col] for col in ['longitude', 'latitude']) for _, row in df.iterrows() ]
    df_flight_paths.drop('longitude', axis=1, inplace=True)
    df_flight_paths.drop('latitude', axis=1, inplace=True)

    # df_flight_paths = df_flight_paths.pivot('flight_id', 'pins')

    df_flight_paths.to_csv('../data/pins')
