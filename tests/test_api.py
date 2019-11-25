import pytest
import time
from perfcounters import PerfCounters
from .fixtures import *  # noqa: F401, F403


def test_len(counters):
    assert len(counters) == len(counters.counters)


def test_get_counter(counters):
    assert counters.get('value') == 42
    assert counters.get('value2') == 43
    assert counters.get('time') > 0.2
    assert counters.get('time2') > 0.2
    assert counters.get('lap') > 0.4


def test_lap_counting(counters):
    assert len(counters.laps['lap']) == 2


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


def test_counter_deadline(caplog):
    cnts = PerfCounters()
    cnts.start('deadline', warning_deadline=1)
    time.sleep(2)
    cnts.stop_all()
    assert "counter deadline deadline exceeded" in caplog.text


def test_counter_logging(caplog):
    cnts = PerfCounters()
    cnts.start('test', log=True)
    assert "test counter started" in caplog.text
    cnts.stop('test', log=True)
    assert "test counter stopped" in caplog.text


def test_time_counters_delta(counters):
    assert counters.get('time') > counters.get('time2')


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
