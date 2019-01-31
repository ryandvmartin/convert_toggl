"""
SpatialCluster package (c) Ryan Martin 2018
"""
from setuptools import setup


if __name__ == '__main__':

    setup(name='convert_toggl',
          version='0.0.1',
          description='Convert toggl csv-dumps to nice formatted spreadsheets',
          maintainer='Ryan Martin',
          maintainer_email='rdm1@ualberta.ca',
          author=['Ryan Martin'],
          license='MIT / CCG',
          packages=['convert_toggl'],
          entry_points={
              # `python setup.py develop` to test with a dev install
              'console_scripts': [
                  'convert_toggl=convert_toggl:main',
              ]
          },
          zip_safe=False)
