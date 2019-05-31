import numpy as np
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
import winsound
plt.style.use('ggplot')

ftimes = pd.read_csv('../data/graphs/fbihours.csv')
dtimes = pd.read_csv('../data/graphs/dhshours.csv')

fig, ax = plt.subplots(1, 1)
ax.plot(ftimes['hour'], ftimes['count'], label='FBI')
ax.plot(dtimes['hour'], dtimes['count'], label='DHS')
ax.set_title("Number of observations over time of day")
ax.set_xlabel("Time of Day")
ax.set_ylabel("Number of Observations")
ax.legend(loc='upper left')

plt.show()

# duration = 500  # seconds
# freq = 440  # Hz
# # os.system(f'play -nq -t alsa synth {duration} sine {freq}')
# winsound.Beep(freq, duration)

def get_times():
    df = pd.read_csv('../data/fulldata')

    fbi_times = '''
                SELECT
                    STRFTIME('%H', timestamp) AS hour,
                    COUNT(STRFTIME('%H', timestamp)) as count
                FROM df
                WHERE 
                    agency = 'fbi'
                GROUP BY STRFTIME('%H', timestamp)
                ORDER BY STRFTIME('%H', timestamp)
                '''

    dhs_times = '''
                SELECT
                    STRFTIME('%H', timestamp) AS hour,
                    COUNT(STRFTIME('%H', timestamp)) as count
                FROM df
                WHERE 
                    agency = 'dhs'
                GROUP BY STRFTIME('%H', timestamp)
                ORDER BY STRFTIME('%H', timestamp)
                '''

    ftimes = ps.sqldf(fbi_times, locals())
    dtimes = ps.sqldf(dhs_times, locals())
    ftimes.to_csv('../data/graphs/fbihours.csv')
    dtimes.to_csv('../data/graphs/dhshours.csv')