import pytest
import time
from perfcounters import PerfCounters


@pytest.fixture()
def counters():
    cnts = PerfCounters()

    cnts.set('value', 42)
    cnts.set('value2', 43)

    cnts.start('lap')

    cnts.start('time')
    time.sleep(0.2)
    cnts.lap('lap')

    cnts.start('time2')
    time.sleep(0.2)
    cnts.lap('lap')

    return cnts
