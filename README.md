# ``convert_toggl``

Utility to process ``toggl`` csv output into timesheets. Collects multiple entries by day into a single entry, rounded to 15 minute intervals.

Installation:

1. Clone Repo

2. If exporting pdf's, follow instructions for [WeazyPrint](https://weasyprint.readthedocs.io/en/latest/install.html#windows).

    * `pip install weasyprint`
    * [install GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

3. Install to local python distribution:

        > python setup.py install

    OR to dev:

        > pip install -e .

4. Configure your name for the exported reports:

    > convert_toggl -name "Ryan Martin"

5. Export a ``.csv`` from the detailed summary, e.g., for last month

    Usage:

        > convert_toggl detailed_toggl_export.csv

    Optionally, with a set of pdf's:

        > convert_toggl -topdf detailed_toggl_export.csv
