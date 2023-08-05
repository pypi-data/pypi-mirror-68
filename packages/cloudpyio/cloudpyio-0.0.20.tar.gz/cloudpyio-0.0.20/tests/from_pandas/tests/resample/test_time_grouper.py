

# -- snippet for {numpy|pandas}_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()

# TODO: use mock.patch() instead of the code below
from pandas.util import testing
def setup_module():
    global old_assert_series_equal
    old_assert_series_equal = testing.assert_series_equal
    def assert_series_equal(*args, **kwargs):
        kwargs['check_series_type'] = False
        return old_assert_series_equal(*args, **kwargs)
    testing.assert_series_equal = assert_series_equal

def teardown_module():
    global old_assert_series_equal
    testing.assert_series_equal = old_assert_series_equal

# -- end {numpy|pandas}_cloud snippet -- #
# pylint: disable=E1101

from datetime import datetime
from operator import methodcaller

import numpy_cloud as np
import pytest

from pandas_cloud.compat import zip

import pandas_cloud as pd
from pandas_cloud import DataFrame, Panel, Series
from pandas_cloud.core.indexes.datetimes import date_range
from pandas_cloud.core.resample import TimeGrouper
import pandas_cloud.util.testing as tm
from pandas_cloud.util.testing import assert_frame_equal, assert_series_equal

test_series = Series(np.random.randn(1000),
                     index=date_range('1/1/2000', periods=1000))


def test_apply():
    with tm.assert_produces_warning(FutureWarning,
                                    check_stacklevel=False):
        grouper = pd.TimeGrouper(freq='A', label='right', closed='right')

    grouped = test_series.groupby(grouper)

    def f(x):
        return x.sort_values()[-3:]

    applied = grouped.apply(f)
    expected = test_series.groupby(lambda x: x.year).apply(f)

    applied.index = applied.index.droplevel(0)
    expected.index = expected.index.droplevel(0)
    assert_series_equal(applied, expected)


def test_count():
    test_series[::3] = np.nan

    expected = test_series.groupby(lambda x: x.year).count()

    with tm.assert_produces_warning(FutureWarning,
                                    check_stacklevel=False):
        grouper = pd.TimeGrouper(freq='A', label='right', closed='right')
    result = test_series.groupby(grouper).count()
    expected.index = result.index
    assert_series_equal(result, expected)

    result = test_series.resample('A').count()
    expected.index = result.index
    assert_series_equal(result, expected)


def test_numpy_reduction():
    result = test_series.resample('A', closed='right').prod()

    expected = test_series.groupby(lambda x: x.year).agg(np.prod)
    expected.index = result.index

    assert_series_equal(result, expected)


def test_apply_iteration():
    # #2300
    N = 1000
    ind = pd.date_range(start="2000-01-01", freq="D", periods=N)
    df = DataFrame({'open': 1, 'close': 2}, index=ind)
    tg = TimeGrouper('M')

    _, grouper, _ = tg._get_grouper(df)

    # Errors
    grouped = df.groupby(grouper, group_keys=False)

    def f(df):
        return df['close'] / df['open']

    # it works!
    result = grouped.apply(f)
    tm.assert_index_equal(result.index, df.index)


@pytest.mark.filterwarnings("ignore:\\nPanel:FutureWarning")
def test_panel_aggregation():
    ind = pd.date_range('1/1/2000', periods=100)
    data = np.random.randn(2, len(ind), 4)

    wp = Panel(data, items=['Item1', 'Item2'], major_axis=ind,
               minor_axis=['A', 'B', 'C', 'D'])

    tg = TimeGrouper('M', axis=1)
    _, grouper, _ = tg._get_grouper(wp)
    bingrouped = wp.groupby(grouper)
    binagg = bingrouped.mean()

    def f(x):
        assert (isinstance(x, Panel))
        return x.mean(1)

    result = bingrouped.agg(f)
    tm.assert_panel_equal(result, binagg)


def test_fails_on_no_datetime_index():
    index_names = ('Int64Index', 'Index', 'Float64Index', 'MultiIndex')
    index_funcs = (tm.makeIntIndex,
                   tm.makeUnicodeIndex, tm.makeFloatIndex,
                   lambda m: tm.makeCustomIndex(m, 2))
    n = 2
    for name, func in zip(index_names, index_funcs):
        index = func(n)
        df = DataFrame({'a': np.random.randn(n)}, index=index)

        msg = ("Only valid with DatetimeIndex, TimedeltaIndex "
               "or PeriodIndex, but got an instance of %r" % name)
        with pytest.raises(TypeError, match=msg):
            df.groupby(TimeGrouper('D'))


def test_aaa_group_order():
    # GH 12840
    # check TimeGrouper perform stable sorts
    n = 20
    data = np.random.randn(n, 4)
    df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    df['key'] = [datetime(2013, 1, 1), datetime(2013, 1, 2),
                 datetime(2013, 1, 3), datetime(2013, 1, 4),
                 datetime(2013, 1, 5)] * 4
    grouped = df.groupby(TimeGrouper(key='key', freq='D'))

    tm.assert_frame_equal(grouped.get_group(datetime(2013, 1, 1)),
                          df[::5])
    tm.assert_frame_equal(grouped.get_group(datetime(2013, 1, 2)),
                          df[1::5])
    tm.assert_frame_equal(grouped.get_group(datetime(2013, 1, 3)),
                          df[2::5])
    tm.assert_frame_equal(grouped.get_group(datetime(2013, 1, 4)),
                          df[3::5])
    tm.assert_frame_equal(grouped.get_group(datetime(2013, 1, 5)),
                          df[4::5])


def test_aggregate_normal():
    # check TimeGrouper's aggregation is identical as normal groupby

    n = 20
    data = np.random.randn(n, 4)
    normal_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    normal_df['key'] = [1, 2, 3, 4, 5] * 4

    dt_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    dt_df['key'] = [datetime(2013, 1, 1), datetime(2013, 1, 2),
                    datetime(2013, 1, 3), datetime(2013, 1, 4),
                    datetime(2013, 1, 5)] * 4

    normal_grouped = normal_df.groupby('key')
    dt_grouped = dt_df.groupby(TimeGrouper(key='key', freq='D'))

    for func in ['min', 'max', 'prod', 'var', 'std', 'mean']:
        expected = getattr(normal_grouped, func)()
        dt_result = getattr(dt_grouped, func)()
        expected.index = date_range(start='2013-01-01', freq='D',
                                    periods=5, name='key')
        assert_frame_equal(expected, dt_result)

    for func in ['count', 'sum']:
        expected = getattr(normal_grouped, func)()
        expected.index = date_range(start='2013-01-01', freq='D',
                                    periods=5, name='key')
        dt_result = getattr(dt_grouped, func)()
        assert_frame_equal(expected, dt_result)

    # GH 7453
    for func in ['size']:
        expected = getattr(normal_grouped, func)()
        expected.index = date_range(start='2013-01-01', freq='D',
                                    periods=5, name='key')
        dt_result = getattr(dt_grouped, func)()
        assert_series_equal(expected, dt_result)

    # GH 7453
    for func in ['first', 'last']:
        expected = getattr(normal_grouped, func)()
        expected.index = date_range(start='2013-01-01', freq='D',
                                    periods=5, name='key')
        dt_result = getattr(dt_grouped, func)()
        assert_frame_equal(expected, dt_result)

    # if TimeGrouper is used included, 'nth' doesn't work yet

    """
    for func in ['nth']:
        expected = getattr(normal_grouped, func)(3)
        expected.index = date_range(start='2013-01-01',
                                    freq='D', periods=5, name='key')
        dt_result = getattr(dt_grouped, func)(3)
        assert_frame_equal(expected, dt_result)
    """


@pytest.mark.parametrize('method, unit', [
    ('sum', 0),
    ('prod', 1),
])
def test_resample_entirly_nat_window(method, unit):
    s = pd.Series([0] * 2 + [np.nan] * 2,
                  index=pd.date_range('2017', periods=4))
    # 0 / 1 by default
    result = methodcaller(method)(s.resample("2d"))
    expected = pd.Series([0.0, unit],
                         index=pd.to_datetime(['2017-01-01',
                                               '2017-01-03']))
    tm.assert_series_equal(result, expected)

    # min_count=0
    result = methodcaller(method, min_count=0)(s.resample("2d"))
    expected = pd.Series([0.0, unit],
                         index=pd.to_datetime(['2017-01-01',
                                               '2017-01-03']))
    tm.assert_series_equal(result, expected)

    # min_count=1
    result = methodcaller(method, min_count=1)(s.resample("2d"))
    expected = pd.Series([0.0, np.nan],
                         index=pd.to_datetime(['2017-01-01',
                                               '2017-01-03']))
    tm.assert_series_equal(result, expected)


@pytest.mark.parametrize('func, fill_value', [
    ('min', np.nan),
    ('max', np.nan),
    ('sum', 0),
    ('prod', 1),
    ('count', 0),
])
def test_aggregate_with_nat(func, fill_value):
    # check TimeGrouper's aggregation is identical as normal groupby
    # if NaT is included, 'var', 'std', 'mean', 'first','last'
    # and 'nth' doesn't work yet

    n = 20
    data = np.random.randn(n, 4).astype('int64')
    normal_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    normal_df['key'] = [1, 2, np.nan, 4, 5] * 4

    dt_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    dt_df['key'] = [datetime(2013, 1, 1), datetime(2013, 1, 2), pd.NaT,
                    datetime(2013, 1, 4), datetime(2013, 1, 5)] * 4

    normal_grouped = normal_df.groupby('key')
    dt_grouped = dt_df.groupby(TimeGrouper(key='key', freq='D'))

    normal_result = getattr(normal_grouped, func)()
    dt_result = getattr(dt_grouped, func)()

    pad = DataFrame([[fill_value] * 4], index=[3],
                    columns=['A', 'B', 'C', 'D'])
    expected = normal_result.append(pad)
    expected = expected.sort_index()
    expected.index = date_range(start='2013-01-01', freq='D',
                                periods=5, name='key')
    assert_frame_equal(expected, dt_result)
    assert dt_result.index.name == 'key'


def test_aggregate_with_nat_size():
    # GH 9925
    n = 20
    data = np.random.randn(n, 4).astype('int64')
    normal_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    normal_df['key'] = [1, 2, np.nan, 4, 5] * 4

    dt_df = DataFrame(data, columns=['A', 'B', 'C', 'D'])
    dt_df['key'] = [datetime(2013, 1, 1), datetime(2013, 1, 2), pd.NaT,
                    datetime(2013, 1, 4), datetime(2013, 1, 5)] * 4

    normal_grouped = normal_df.groupby('key')
    dt_grouped = dt_df.groupby(TimeGrouper(key='key', freq='D'))

    normal_result = normal_grouped.size()
    dt_result = dt_grouped.size()

    pad = Series([0], index=[3])
    expected = normal_result.append(pad)
    expected = expected.sort_index()
    expected.index = date_range(start='2013-01-01', freq='D',
                                periods=5, name='key')
    assert_series_equal(expected, dt_result)
    assert dt_result.index.name == 'key'


def test_repr():
    # GH18203
    result = repr(TimeGrouper(key='A', freq='H'))
    expected = ("TimeGrouper(key='A', freq=<Hour>, axis=0, sort=True, "
                "closed='left', label='left', how='mean', "
                "convention='e', base=0)")
    assert result == expected


@pytest.mark.parametrize('method, unit', [
    ('sum', 0),
    ('prod', 1),
])
def test_upsample_sum(method, unit):
    s = pd.Series(1, index=pd.date_range("2017", periods=2, freq="H"))
    resampled = s.resample("30T")
    index = pd.to_datetime(['2017-01-01T00:00:00',
                            '2017-01-01T00:30:00',
                            '2017-01-01T01:00:00'])

    # 0 / 1 by default
    result = methodcaller(method)(resampled)
    expected = pd.Series([1, unit, 1], index=index)
    tm.assert_series_equal(result, expected)

    # min_count=0
    result = methodcaller(method, min_count=0)(resampled)
    expected = pd.Series([1, unit, 1], index=index)
    tm.assert_series_equal(result, expected)

    # min_count=1
    result = methodcaller(method, min_count=1)(resampled)
    expected = pd.Series([1, np.nan, 1], index=index)
    tm.assert_series_equal(result, expected)

    # min_count>1
    result = methodcaller(method, min_count=2)(resampled)
    expected = pd.Series([np.nan, np.nan, np.nan], index=index)
    tm.assert_series_equal(result, expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
