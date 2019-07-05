# convert_toggl

Utility to process toggl csv output into billable timesheets. Collects multiple entries by day into a single entry, rounded to 15 minute intervals.

Installation:

1. Clone Repo

2. Modify `myname` in `convert_toggl/convert_toggl.py`

3. Install to local python distribution:

        > python setup.py install

    OR to dev:

        > pip install -e .

    Usage:

        > convert_toggl detailed_toggl_export.csv

Currently separate tables are export by `Project` field.
