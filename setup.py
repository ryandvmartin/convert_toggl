"""
Convert Toggl (c) Ryan Martin 2019

`pip install -e .` to get going
"""
from setuptools import setup


if __name__ == "__main__":

    setup(
        name="convert_toggl",
        version="0.0.3",
        description="Convert toggl csv-dumps to nice formatted spreadsheets",
        maintainer="Ryan Martin",
        maintainer_email="rdm1@ualberta.ca",
        author=["Ryan Martin"],
        license="MIT / CCG",
        packages=["convert_toggl"],
        package_requires=["python=3", "pandas", "xlsxwriter"],
        entry_points={
            "console_scripts": [
                "convert_toggl=convert_toggl:main",
            ]
        },
        zip_safe=False,
    )
