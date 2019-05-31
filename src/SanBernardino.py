import numpy as np
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import winsound
plt.style.use('ggplot')

fdays = pd.read_csv('../data/graphs/fdays.csv')
fdays['date'] = fdays[['month', 'day']].apply(lambda x: ' '.join(str(x)), axis=1)
ddays = pd.read_csv('../data/graphs/ddays.csv')
ddays['date'] = ddays[['month', 'day']].apply(lambda x: ' '.join(str(x)), axis=1)

fig, ax = plt.subplots(1, 1)
ax.plot(fdays['date'], fdays['count'], label='FBI')
ax.plot(fdays['date'], ddays['count'], label='DHS')
ax.set_title("Number of Observations within 2 months of the San Bernardino Attack")
ax.set_xlabel("Day")
ax.set_ylabel("Number of Observations")
ax.legend(loc='upper left')
ax.axvline(fdays['date'][28], ls='--', color='black')

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=(1,15)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.show()

def makedaycsvs():
    df = pd.read_csv('../data/fulldata')

    fbi_days = '''
                SELECT
                    STRFTIME('%m', timestamp) AS month,
                    STRFTIME('%d', timestamp) AS day,
                    COUNT(*) as count
                FROM df
                WHERE 
                    agency = 'fbi'
                    AND latitude > 33
                    AND latitude < 35
                    AND STRFTIME('%m', timestamp) >= '11'
                GROUP BY 
                    STRFTIME('%m', timestamp),
                    STRFTIME('%d', timestamp)
                ORDER BY 
                    STRFTIME('%m', timestamp),
                    STRFTIME('%d', timestamp)
                '''

    dhs_days = '''
                SELECT
                    STRFTIME('%m', timestamp) AS month,
                    STRFTIME('%d', timestamp) AS day,
                    COUNT(*) as count
                FROM df
                WHERE 
                    agency = 'dhs'
                    AND latitude > 33
                    AND latitude < 35
                    AND STRFTIME('%m', timestamp) >= '11'
                GROUP BY 
                    STRFTIME('%m', timestamp),
                    STRFTIME('%d', timestamp)
                ORDER BY 
                    STRFTIME('%m', timestamp),
                    STRFTIME('%d', timestamp)
                '''

    fdays = ps.sqldf(fbi_days, locals())
    ddays = ps.sqldf(dhs_days, locals())
    fdays.to_csv('../data/graphs/fdays.csv')
    ddays.to_csv('../data/graphs/ddays.csv')