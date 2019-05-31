import pandas as pd
import pandasql as ps
import plotly.plotly as py
import plotly.graph_objs as go
import os

def fetch_locations(filename='../data/days/2015-08-17.csv'):
    df_flight_paths = pd.read_csv(filename)
    flight_query = '''
                    SELECT
                        flight_id,
                        longitude,
                        latitude
                    FROM df_flight_paths
                    '''
    return ps.sqldf(flight_query, locals())

    # df_flight_paths = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv')
    # df_flight_paths.head()

def plot_one_day(filename):
    df_flight_paths = fetch_locations(f'../data/days/{filename}').values
    flights = {}
    for row in df_flight_paths:
        if row[0] not in flights:
            flights[row[0]] = [row[1], row[2]]
        else:
            flights[row[0]] = [flights[row[0]][0], flights[row[0]][1], row[1], row[2]]

    df_airports = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

    airports = [go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_airports['long'],
        lat = df_airports['lat'],
        hoverinfo = 'text',
        text = df_airports['airport'],
        mode = 'markers',
        marker = go.scattergeo.Marker(
            size = 2,
            color = 'rgb(255, 0, 0)',
            line = go.scattergeo.marker.Line(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        ))]

    flight_paths = []
    for flight in flights.values():

        if len(flight) == 2:
            continue

        flight_paths.append(
            go.Scattergeo(
                locationmode = 'USA-states',
                lon = [flight[0], flight[2]],
                lat = [flight[1], flight[3]],
                mode = 'lines',
                line = go.scattergeo.Line(
                    width = 1,
                    color = 'red',
                ),
                # opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
            )
        )

    layout = go.Layout(
        title = go.layout.Title(
            text = 'Federal Flight Paths'
        ),
        showlegend = False,
        geo = go.layout.Geo(
            scope = 'north america',
            projection = go.layout.geo.Projection(type = 'azimuthal equal area'),
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )

    fig = go.Figure(data = flight_paths + airports, layout = layout)
    py.iplot(fig, filename = filename)

directory = '../data/days'

files = os.listdir(directory)
files.sort()
count = 1
for filename in files:
    count += 1
    plot_one_day(filename)
    if count % 20 == 0:
        input("Press Enter to continue...")

duration = .5  # seconds
freq = 440  # Hz
os.system(f'play -nq -t alsa synth {duration} sine {freq}')
