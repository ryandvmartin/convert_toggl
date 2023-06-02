"""Convert toggle exports, optionally by project"""
# flake8: noqa


import argparse
import os

import pandas as pd

pd.set_option("display.max_colwidth", None)


THISDIR = os.path.abspath(os.path.dirname(__file__))


def set_name(name):
    """Set ``name`` to disk"""
    with open(os.path.join(THISDIR, "name.txt"), "w") as fh:
        fh.write(name.strip())


def get_name():
    """Get a name from the stored file"""
    try:
        with open(os.path.join(THISDIR, "name.txt"), "r") as fh:
            return fh.read().strip()
    except Exception:
        set_name("MY NAME")
        return "MY NAME"


def round_to_nearest_15(value):
    """Round the value to the nearest 15 minutes

    eg. 3h:17m->3h:15m,  3.28hr -> 3.25hr
    """
    step = pd.Timedelta("00:15:00")
    return step * round(pd.Timedelta(value) / step)


def convert_merge_time_entries(df: pd.DataFrame):
    """Get each time entry, merge ead day and round"""
    df["Duration"] = df["Duration"].apply(pd.Timedelta)
    data = []
    myname = get_name()
    for date in sorted(set(df["Start date"])):
        dfslice = df.loc[df["Start date"] == date]
        unrounded_hours = dfslice["Duration"].sum()
        hours_worked = round_to_nearest_15(unrounded_hours)
        tasks = ", ".join([task for task in set(dfslice["Description"])])
        data.append(
            [
                date,
                myname,
                hours_worked.total_seconds() / 3600,
                unrounded_hours.total_seconds() / 3600,
                tasks,
            ]
        )
    df = pd.DataFrame(
        data, columns=["Date", "Employee", "Hours", "Unrounded Hours", "Description"]
    )
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Date").reset_index(drop=True)


def get_all_tables(all_toggl_df):
    """Get a dictionary of id: table"""
    tables = {}
    if "project" in [c.lower() for c in all_toggl_df.columns]:
        for projectid, subdf in list(all_toggl_df.groupby("Project")):
            out_table = convert_merge_time_entries(subdf)
            tables[projectid] = out_table
    else:
        out_table = convert_merge_time_entries(all_toggl_df)
        tables[None] = out_table
    return tables


def write_sectioned_xlsx(tables, outfile):  # noqa
    """Export tables to a single excel file"""
    import xlsxwriter

    wb = xlsxwriter.Workbook(outfile.replace("csv", "xlsx"))
    sheet = wb.add_worksheet()
    sheet.set_landscape()
    header = wb.add_format({"bold": True, "font_color": "blue", "font_size": 15})
    table_header = wb.add_format({"bold": True, "top": False, "bottom": True})
    table_footer = wb.add_format(
        {
            "bold": True,
            "top": True,
            "align": "center",
            "valign": "vcenter",
            "num_format": "#,##0.00",
        }
    )
    base = wb.add_format(
        {"align": "center", "valign": "vcenter", "num_format": "#,##0.00"}
    )
    bold_base = wb.add_format(
        {"align": "center", "valign": "vcenter", "bold": True, "num_format": "#,##0.00"}
    )
    date = wb.add_format(
        {"num_format": "yyyy/mm/dd", "align": "center", "valign": "vcenter"}
    )
    wrap = wb.add_format({"align": "left", "valign": "vcenter", "text_wrap": True})
    widths = [12, 12, 8, 17, 90]
    for icol, width in enumerate(widths):
        sheet.set_column(icol, icol, width)
    irow = 0
    total_hours = 0.0
    total_unrounded = 0.0
    for pid, df in tables.items():
        sheet.write(irow, 0, pid, header)
        irow += 1
        for icol, col in enumerate(df.columns):
            sheet.write(irow, icol, col, table_header)
        irow += 1
        df = df.sort_values("Date")
        for irow_table in range(len(df)):
            for icol, col in enumerate(df.columns):
                if col == "Date":
                    fmt = date
                elif col == "Description":
                    fmt = wrap
                elif "hours" in col.lower():
                    fmt = base
                else:
                    fmt = wb.add_format({"align": "center", "valign": "vcenter"})
                val = df.loc[irow_table, col]
                sheet.write(irow, icol, val, fmt)
            irow += 1
        for icol in [0, 4]:
            sheet.write(irow, icol, " ", table_footer)
        sheet.write(
            irow,
            1,
            "Total:",
            wb.add_format({"bold": True, "align": "right", "top": True}),
        )
        total_hours += df["Hours"].sum()
        sheet.write(irow, 2, df["Hours"].sum(), table_footer)
        total_unrounded += df["Unrounded Hours"].sum()
        sheet.write(irow, 3, df["Unrounded Hours"].sum(), table_footer)
        irow += 3
    sheet.write(
        irow, 1, "Monthly Total:", wb.add_format({"bold": True, "align": "right"})
    )
    sheet.write(irow, 2, total_hours, bold_base)
    sheet.write(irow, 3, total_unrounded, bold_base)
    sheet.fit_to_pages(1, 2)
    wb.close()


def write_csvs(tables, outfile):
    """Export csv tables"""
    for pid, df in tables.items():
        prefix = "" if pid is None else pid.lower() + "-"
        df.to_csv(f"{prefix}{outfile}", index=False)


def convert_toggl_export(toggl_export, outfile, xlsx=False):
    """Read through an exported toggle file and save by project"""
    if outfile.endswith("xls") or outfile.endswith("xlsx"):
        xlsx = True
    df = pd.read_csv(toggl_export)
    tables = get_all_tables(df)
    if xlsx:
        write_sectioned_xlsx(tables, outfile)
    else:
        write_csvs(tables, outfile)


def main():
    """Run the toggl - exporter"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "toggle_export_csv", nargs="?", type=str, help="The name of the toggl csv"
    )
    parser.add_argument(
        "processed_csv",
        nargs="?",
        type=str,
        default="out.csv",
        help="The output csv file",
    )
    parser.add_argument(
        "-name",
        type=str,
        nargs="?",
        default=None,
        help='Set a default name with "MY NAME"',
    )
    parser.add_argument(
        "-xlsx", action="store_true", help="Export a sectioned excel file"
    )
    args = parser.parse_args()
    if args.name:
        print(f"Setting ``NAME`` == '{args.name}'")
        set_name(args.name)
    else:
        convert_toggl_export(args.toggle_export_csv, args.processed_csv, args.xlsx)


if __name__ == "__main__":
    main()
