import pandas as pd
import argparse

myname = 'Ryan Martin'


def convert_toggl(toggl_export, csvoutfile):
    df = pd.read_csv(toggl_export)
    df['Duration'] = df['Duration'].apply(pd.Timedelta).dt.round('15min')
    data = []
    for date in sorted(set(df['Start date'])):
        dfslice = df.loc[df['Start date'] == date]
        hours_worked = dfslice['Duration'].sum()
        tasks = ', '.join([task for task in set(dfslice['Description'])]).capitalize()
        data.append([date, myname, tasks, hours_worked.total_seconds() / 3600])
    hourtable = pd.DataFrame(data, columns=['Date', 'Employee', 'Description', 'Hours'])
    hourtable.to_csv(csvoutfile, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('toggl_file', type=str, help='The name of the toggl csv')
    parser.add_argument('out_file', type=str, help='The output csv file')
    args = parser.parse_args()
    convert_toggl(args.toggl_file, args.out_file)


if __name__ == '__main__':
    main()
