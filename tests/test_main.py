import pytest
import time
import json
from perfcounters import PerfCounters


@pytest.fixture(scope="module")
def counters():
    cnts = PerfCounters()

    cnts.set('value', 42)
    cnts.set('value2', 43)

    cnts.start('time')
    time.sleep(0.2)

    cnts.start('time2')
    time.sleep(0.2)
    return cnts


def test_len(counters):
    l = len(counters.counters)
    assert len(counters) == l


def test_get_counter(counters):
    assert counters.get('value') == 42
    assert counters.get('value2') == 43
    assert counters.get('time') > 0
    assert counters.get('time2') > 0


def test_set_counter(counters):
    counters.set('set', 42)
    assert counters.get('set') == 42


def test_increment_counter(counters):
    counters.set('inc', 1)
    assert counters.get('inc') == 1
    counters.increment('inc')
    assert counters.get('inc') == 2
    counters.increment('inc', 40)
    assert counters.get('inc') == 42


def test_direct_increment(counters):
    counters.increment('inc2', 42)
    assert counters.get('inc2') == 42


def test_get_empty_counter(counters):
    assert not counters.get('donotexist')


def test_time_counters(counters):
    assert counters.counters['time']['start'] > 0
    counters.stop('time')
    assert counters.counters['time']['stop'] > 0
    assert counters.get('time') > 0


def test_time_counters_delta(counters):
    assert counters.get('time') + 1 > counters.get('time2')


def test_stop_all(counters):
    counters.stop_all()
    assert counters.counters['time']['stop'] > 0
    assert counters.counters['time2']['stop'] > 0


def test_dup_timing_counters(counters):
    with pytest.raises(ValueError):
        counters.start('time')


def test_error_on_non_started_counters(counters):
    with pytest.raises(ValueError):
        counters.stop('error')


def test_to_json_values(counters):
    js = counters.to_json()
    cnts = json.loads(js)
    assert 'Timing counters' in cnts
    assert 'Value counters' in cnts
    # by default counters are in reverse order
    assert cnts['Value counters'][1][0] == 'value'
    assert cnts['Value counters'][1][1] == 42


def test_to_json_time(counters):
    js = counters.to_json()
    cnts = json.loads(js)
    assert 'Value counters' in cnts
    assert 'Timing counters' in cnts
    assert cnts['Timing counters'][0][0] == 'time'


def test_to_html(counters):
    html = counters.to_html()
    assert '<tr><td>value </td>' in html
    assert '<td style="text-align: right;">     42</td></tr>' in html
    assert 'Value counters' in html


def test_output(counters, capsys):
    counters.report()
    out, _ = capsys.readouterr()
    assert "\n+========+=========+\n| value2 |      43 |\n" in out


def test_log(counters, caplog):
    counters.log()
    txt = caplog.text
    assert "value:42" in txt


def test_counter_sorting():
    cnts = PerfCounters()  # clean instance
    cnts.set('a', 42)
    cnts.set('b', 43)

    # value desc (default)
    dic = cnts._get_counter_lists()
    assert dic['Value counters'][0][1] > dic['Value counters'][1][1]

    # value asc
    dic = cnts._get_counter_lists(reverse=False)
    assert dic['Value counters'][0][1] < dic['Value counters'][1][1]

    # name desc
    dic = cnts._get_counter_lists(sort_by=PerfCounters.SORT_BY_NAME)
    assert dic['Value counters'][0][0] == 'b'

    # name asc
    dic = cnts._get_counter_lists(sort_by=PerfCounters.SORT_BY_NAME,
                                  reverse=False)
    assert dic['Value counters'][0][0] == 'a'


def test_merge(counters):
    counters2 = PerfCounters()
    counters2.set('value3', 44)
    counters.merge(counters2)
    assert 'value3' in counters.counters
    assert counters.get('value3') == 44


def test_duplicate_merge(counters):
    counters2 = PerfCounters()
    counters2.set('value', 44)
    with pytest.raises(ValueError):
        counters.merge(counters2)


def test_prefix_counter():
    cnts = PerfCounters()
    v = cnts._prefix_counter('test')
    assert v == 'test'
    cnts = PerfCounters('prefix')
    v = cnts._prefix_counter('test')
    assert v == 'prefix_test'
