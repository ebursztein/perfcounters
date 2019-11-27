import time
from perfcounters import PerfCounters
from perfcounters.report import process_counters, _gen_header
from perfcounters.report import TIME_COUNTERS, VALUE_COUNTERS, LAPS_COUNTERS

from .fixtures import *  # noqa: F401, F403


def test_counter_delta_auto_closing():
    cnts = PerfCounters()
    cnts.start('tmp')
    cnts.start('lap')
    time.sleep(0.2)
    cnts.lap('lap')
    cnts.start('tmp2')
    time.sleep(0.2)
    cnts.lap('lap')
    cnts.stop('tmp')

    time.sleep(0.1)
    cnts.stop('lap')

    dic = process_counters(cnts.counters, cnts.laps)

    assert len(dic[TIME_COUNTERS]) == 3  # 2 time + lap
    assert len(dic[LAPS_COUNTERS]) == 1
    assert dic[TIME_COUNTERS][0][0] == 'lap'
    assert dic[TIME_COUNTERS][0][1] >= 0.5
    assert dic[TIME_COUNTERS][1][0] == 'tmp'
    assert dic[TIME_COUNTERS][1][1] >= 0.4
    assert dic[TIME_COUNTERS][2][0] == 'tmp2'
    assert dic[TIME_COUNTERS][2][1] >= 0.2


def test_no_lap():
    cnts = PerfCounters()
    cnts.start('tmp')
    dic = process_counters(cnts.counters, cnts.laps)
    assert LAPS_COUNTERS not in dic


def test_process_counters_values():
    cnts = PerfCounters()
    cnts.set('value', 42)
    cnts.set('value2', 43)
    dic = process_counters(cnts.counters, cnts.laps, sort_by='name',
                           reverse=False)
    assert len(dic[VALUE_COUNTERS]) == 2
    assert dic[VALUE_COUNTERS][0][0] == 'value'
    assert dic[VALUE_COUNTERS][0][1] == 42
    assert dic[VALUE_COUNTERS][1][0] == 'value2'
    assert dic[VALUE_COUNTERS][1][1] == 43


def test_counter_value_desc_sorting(counters):
    # value desc (default)
    dic = process_counters(counters.counters, counters.laps)
    assert dic[VALUE_COUNTERS][0][1] > dic[VALUE_COUNTERS][1][1]


def test_counter_value_asc_sorting(counters):
    dic = process_counters(counters.counters, counters.laps, sort_by='value',
                           reverse=False)
    assert dic[VALUE_COUNTERS][0][1] < dic[VALUE_COUNTERS][1][1]


def test_counter_name_desc_sorting(counters):
    dic = process_counters(counters.counters, counters.laps, sort_by='name',
                           reverse=True)
    assert dic[VALUE_COUNTERS][0][0] == 'value2'


def test_counter_name_asc_sorting(counters):
    dic = process_counters(counters.counters, counters.laps, sort_by='name',
                           reverse=False)
    assert dic[VALUE_COUNTERS][0][0] == 'value'


def test_gen_html_header():
    assert "<h1>test</h1>" in _gen_header('test', 1, 'html')
    assert "<h2>test2</h2>" in _gen_header('test2', 2, 'html')


def test_gen_text_header():
    assert "-=[test]=-" in _gen_header('test', 1, 'text')
    assert "test2" in _gen_header('test2', 2, 'text')


def test_gen_markdown_header():
    assert "#test" in _gen_header('test', 1, 'markdown')
    assert "##test2" in _gen_header('test2', 2, 'markdown')
