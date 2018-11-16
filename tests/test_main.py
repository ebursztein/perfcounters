import pytest
import time
import json
from PerfCounters import PerfCounters

@pytest.fixture()
def counters():
    counters = PerfCounters()
    return counters

def test_set_counter(counters):
    counters.set('test', 42)
    assert counters.get('test') == 42

def test_get_empty_counter(counters):
    assert counters.get('test') == None

def test_time_counters(counters):
    counters.start('test')
    time.sleep(1)
    counters.stop('test')
    assert counters.get('test') > 1 and counters.get('test') < 2

def test_error_on_non_started_counters(counters):
    with pytest.raises(ValueError):
        counters.stop('error')

def test_to_json_values(counters):
    counters.set('cnt1', 42)
    js = counters.to_json()
    cnts = json.loads(js)
    assert 'Timing counters' not in cnts    
    assert 'Value counters' in cnts
    assert cnts['Value counters'][0][0] == 'cnt1'
    assert cnts['Value counters'][0][1] == 42

def test_to_json_time(counters):
    counters.start('tmt1')
    counters.stop('tmt1')
    js = counters.to_json()
    cnts = json.loads(js)
    assert 'Value counters' not in cnts
    assert 'Timing counters' in cnts    
    assert cnts['Timing counters'][0][0] == 'tmt1'