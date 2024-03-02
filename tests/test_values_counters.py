import pytest
from perfcounters.value_counters import ValueCounters


def test_prefix():
    cnt_name = "test_a"
    cnts = ValueCounters(prefix='test_')
    cnts.set('a', 53)
    clst = cnts.get_all()
    assert cnt_name in clst
    cnt = cnts.counters['a']
    assert str(cnt) == cnt_name
    assert cnt.__repr__() == cnt_name

def test_e2e_float():
    cnts = ValueCounters()
    cnts.inc('a', 4.2)
    assert cnts.get('a') == 4.2
    assert cnts.get('a', rounding=0) == 4


def test_e2e():
    cnts = ValueCounters()
    cnts.inc('a', 42)
    assert cnts.get('a') >= 42
    cnts.dec('a', 2)
    assert cnts.get('a') == 40
    cnts.set('a', 2)
    assert cnts.get('a') == 2
    cnt = cnts.counters['a']
    assert str(cnt) == 'a'
    assert cnt.__repr__() == 'a'

    cnts.inc('b', 2)
    assert len(cnts) == 2

def test_dec():
    cnts = ValueCounters()
    cnts.dec('a', 2)
    assert cnts.get('a') == -2



def test_laps():
    cnts = ValueCounters()
    cnts.set('a', value=10)
    cnts.lap('a')
    cnts.inc('a', 10)
    assert cnts.get('a') == 20
    assert len(cnts.get_laps('a')) == 2

    cnts.lap('b')
    assert cnts.get('b') == 0
    assert len(cnts.get_laps('b')) == 2

def test_wrong_get_lap():
    with pytest.raises(ValueError):
        cnts = ValueCounters()
        cnts.set('a', 20)
        cnts.get_laps('b')


def test_wrong_get_name():
    with pytest.raises(ValueError):
        cnts = ValueCounters()
        cnts.set('a')
        cnts.get('b')

def test_reset_wrong_name():
    with pytest.raises(ValueError):
        cnts = ValueCounters()
        cnts.reset('a')


def test_double_exist():
    with pytest.raises(ValueError):
        cnts = ValueCounters()
        cnts._init_counter('a')
        cnts._init_counter('a')


def test_reset():
    cnts = ValueCounters()
    cnts.set('a', value=32)
    assert cnts.get('a') == 32
    cnts.reset('a')
    assert cnts.get('a') == 0

def test_reset_all():
    cnts = ValueCounters()
    cnts.set('a', value=32)
    cnts.set('b', value=33)
    assert cnts.get('a') == 32
    assert cnts.get('b') == 33

    cnts.reset_all()
    assert cnts.get('a') == 0
    assert cnts.get('b') == 0


def test_report():
    cnts = ValueCounters()
    cnts.set('a', value=32)
    cnts.set('b', value=33)
    assert 'b' in cnts.to_json()
    assert 'b' in cnts.to_html()
    assert 'b' in cnts.to_latex()
    assert 'b' in cnts.to_md()

    cnts.report()