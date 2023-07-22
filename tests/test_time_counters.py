from time import sleep
from perfcounters import TimeCounters


def test_e2e():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    cnts.start('b')
    sleep(D)
    cnts.stop('a')
    assert cnts.get('a') >= D
    sleep(D)
    assert cnts.get('a') < cnts.get('b')


def test_format_ms():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
