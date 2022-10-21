# ``convert_toggl``

Utility to process ``toggl`` csv output into timesheets. Collects multiple entries by day into a single entry, rounded to 15 minute intervals.

Installation:

1. Clone and install to local python distribution:

        > python setup.py install

    OR to dev:

        > pip install -e .

2. Configure your name for the exported reports:

    > convert_toggl -name "My Name"

3. From the toggl web interface, go to `Reports`, export a csv from the `Detailed` tab for a given date range.

4. Export a ``.csv`` from the detailed summary, e.g., for last month:

    > convert_toggl detailed_toggl_export.csv

5. Export a ``.xlsx`` from the detailed summary (requires `pip install xlsxwriter`):

    > convert_toggl detailed_toggl_export.csv TimeSheets.xlsx
