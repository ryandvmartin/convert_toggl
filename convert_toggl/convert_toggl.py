"""Convert toggle exports, optionally by project"""
import argparse
import os

import pandas as pd
pd.set_option('display.max_colwidth', -1)

THISDIR = os.path.abspath(os.path.dirname(__file__))


def save_table(data: pd.DataFrame, outfile, name=None, project=None):
    """Render a table to pdf using jinja2 templates"""
    from jinja2 import Environment, FileSystemLoader
    from weasyprint import HTML
    env = Environment(loader=FileSystemLoader(THISDIR))
    template = env.get_template('table_template.html')
    if name is None:
        name = get_name()
    if project:
        table_title = f'{name} - Hours - {project}'
    else:
        table_title = f'{name} - Hours'
    data = data[['Date', 'Employee', 'Hours', 'Description']]
    html_table = data.to_html(index=False, float_format='%.2f',
                              justify='left')
    template_vars = {'title': 'Time Sheet',
                     'table_title': table_title,
                     'hours_table': html_table}
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(outfile, stylesheets=[
        os.path.join(THISDIR, 'style.css')])


def set_name(name):
    """Set ``name`` to disk"""
    with open(os.path.join(THISDIR, 'name.txt'), 'w') as fh:
        fh.write(name.strip())


def get_name():
    """Get a name from the stored file"""
    try:
        with open(os.path.join(THISDIR, 'name.txt'), 'r') as fh:
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


def convert_toggl_export(toggl_export, outfile, topdf=False):
    """Read through an exported toggle file and save by project"""
    df = pd.read_csv(toggl_export)
    if 'project' in [c.lower() for c in df.columns]:
        for projectid, subdf in list(df.groupby('Project')):
            out_table = convert_merge_time_entries(subdf)
            out_table.to_csv(f'{projectid.lower()}-{outfile}', index=False)
            if topdf:
                save_table(out_table, f'{projectid.lower()}-{outfile}.pdf',
                           project=projectid)
    else:
        out_table = convert_merge_time_entries(df)
        out_table.to_csv(outfile, index=False)
        if topdf:
            save_table(out_table, f'{projectid.lower()}-{outfile}.pdf')


def main():
    """Run the toggl-exporter"""
    parser = argparse.ArgumentParser()
    parser.add_argument('toggle_export_csv', nargs='?', type=str,
                        help='The name of the toggl csv')
    parser.add_argument('processed_csv', nargs='?', type=str, default='out.csv',
                        help='The output csv file')
    parser.add_argument('-name', type=str, nargs='?', default=None,
                        help='Set a default name with "MY NAME"')
    parser.add_argument('-topdf', action='store_true', help='Export a formatted pdf')
    args = parser.parse_args()
    if args.name:
        print(f"Setting ``NAME`` == '{args.name}'")
        set_name(args.name)
    else:
        convert_toggl_export(args.toggle_export_csv, args.processed_csv, args.topdf)


if __name__ == '__main__':
    main()
