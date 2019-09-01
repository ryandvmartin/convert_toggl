"""Convert toggle exports, optionally by project"""
import argparse
import os

import pandas as pd


def set_name(name):
    """Set ``name`` to disk"""
    with open(os.path.join(os.path.dirname(__file__), 'name.txt'), 'w') as fh:
        fh.write(name.strip())


def get_name():
    """Get a name from the stored file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'name.txt'), 'r') as fh:
            return fh.read().strip()
    except Exception:
        set_name("MY NAME")
        return "MY NAME"


def round_to_nearest_15(value):
    """Round the value to the nearest 15 minutes, eg. 3:17 -> 3:15,  3:22 -> 3:25"""
    step = pd.Timedelta('00:15:00')
    return step * round(pd.Timedelta(value) / step)


def convert_merge_time_entries(df: pd.DataFrame):
    """Get each time entry, merge ead day and round"""
    df['Duration'] = df['Duration'].apply(pd.Timedelta)
    data = []
    myname = get_name()
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
    """Read through an exported toggle file and save by project"""
    df = pd.read_csv(toggl_export)
    if 'project' in [c.lower() for c in df.columns]:
        for projectid, subdf in list(df.groupby('Project')):
            out_table = convert_merge_time_entries(subdf)
            out_table.to_csv(f'{projectid.lower()}-{outfile}', index=False)
    else:
        out_table = convert_merge_time_entries(df)
        out_table.to_csv(outfile, index=False)


def main():
    """Run the toggl-exporter"""
    parser = argparse.ArgumentParser()
    parser.add_argument('toggle_export_csv', nargs='?', type=str,
                        help='The name of the toggl csv')
    parser.add_argument('processed_csv', nargs='?', type=str, default='out.csv',
                        help='The output csv file')
    parser.add_argument('-name', type=str, nargs='?', default=None,
                        help='Set a default name with "MY NAME"')
    parser.add_argument('-to-pdf', action='store_true', help='Export a formatted pdf')
    args = parser.parse_args()
    if args.name:
        print(f"Setting ``NAME`` == '{args.name}'")
        set_name(args.name)
    else:
        convert_toggl_export(args.toggle_export_csv, args.processed_csv)


if __name__ == '__main__':
    main()
