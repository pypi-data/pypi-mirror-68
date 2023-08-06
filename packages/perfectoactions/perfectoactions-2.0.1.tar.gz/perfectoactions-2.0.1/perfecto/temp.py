import tzlocal
import pandas
import datetime as dt
data = {'startTime':  ['1589285837249'], 'endTime':  ['1589285948199']
        }

df = pandas.DataFrame (data, columns = ['startTime','endTime'])
print(tzlocal.get_localzone())
df['startTime'] = pandas.to_datetime(df['startTime'].astype(int), unit='ms')
df['startTime'] = df['startTime'].dt.tz_localize('utc').dt.tz_convert(tzlocal.get_localzone())
df['startTime'] = df['startTime'].dt.strftime('%d/%m/%Y %H:%M:%S')

df['endTime'] = pandas.to_datetime(df['endTime'].astype(int), unit='ms')
df['endTime'] = df['endTime'].dt.tz_localize('utc').dt.tz_convert(tzlocal.get_localzone())
df['endTime'] = df['endTime'].dt.strftime('%d/%m/%Y %H:%M:%S')

df['A'] = pandas.to_datetime(df['startTime'])
df['B'] = pandas.to_datetime(df['endTime'])
df['Duration'] = (pandas.to_datetime(df['endTime']) - pandas.to_datetime(df['startTime'])).dt.date
print(df)
