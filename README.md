# convert_toggl
Utility to process toggl csv output into billable timesheets. Collects multiple entries by day into
a single entry, rounded to 15 minute intervals.

Install with:

> python setup.py install

Usage:

> convert_toggl csvin.csv csvout.csv
