from perfcounters import ValueCounters


def test_e2e():
    D = 0.2
    cnts = ValueCounters()
    cnts.start('a')
    cnts.inc('a', 42)
    assert cnts.get('a') >= 42
    cnts.dec('a', 2)
    assert cnts.get('a') == 40
