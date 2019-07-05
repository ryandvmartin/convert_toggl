

import convert_toggl
import pandas as pd


def test_rounding():
    assert convert_toggl.round_to_nearest_15('00:25:00') == pd.Timedelta('00:30:00')
    assert convert_toggl.round_to_nearest_15('00:15:00') == pd.Timedelta('00:15:00')
    assert convert_toggl.round_to_nearest_15('15:05:00') == pd.Timedelta('15:00:00')


def test_convert_export():
    df = pd.read_csv('./toggl-export.csv')
    converted = convert_toggl.convert_merge_time_entries(df)
    assert all(c in converted.columns for c in ['Date', 'Employee', 'Hours', 'Unrounded_hours',
                                                'Description'])
