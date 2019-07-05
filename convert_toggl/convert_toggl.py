import pandas as pd
import argparse

myname = 'Ryan Martin'


def round_to_nearest_15(value):
    """Round the value to the nearest 15 minutes, eg. 3:17 -> 3:15,  3:22 -> 3:25"""
    step = pd.Timedelta('00:15:00')
    return step * round(pd.Timedelta(value) / step)


def convert_merge_time_entries(df: pd.DataFrame):
    df['Duration'] = df['Duration'].apply(pd.Timedelta)
    data = []
    for date in sorted(set(df['Start date'])):
        dfslice = df.loc[df['Start date'] == date]
        hours_worked = round_to_nearest_15(dfslice['Duration'].sum())
        unrounded_hours = dfslice['Duration'].sum()
        tasks = ', '.join([task for task in set(dfslice['Description'])]).capitalize()
        data.append([date, myname, hours_worked.total_seconds() / 3600,
                     unrounded_hours.total_seconds() / 3600, tasks])
    return pd.DataFrame(data, columns=['Date', 'Employee', 'Hours', 'Unrounded_hours',
                                       'Description'])


def convert_toggl_export(toggl_export, outfile):
    df = pd.read_csv(toggl_export)
    if 'project' in [c.lower() for c in df.columns]:
        for projectid, subdf in list(df.groupby('Project')):
            out_table = convert_merge_time_entries(subdf)
            out_table.to_csv(f'{projectid.lower()}-{outfile}', index=False)
    else:
        out_table = convert_merge_time_entries(df)
        out_table.to_csv(outfile, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('toggle_export_csv', type=str, help='The name of the toggl csv')
    parser.add_argument('processed_csv', nargs='?', type=str, default='out.csv',
                        help='The output csv file')
    args = parser.parse_args()
    convert_toggl_export(args.toggle_export_csv, args.processed_csv)


if __name__ == '__main__':
    main()
