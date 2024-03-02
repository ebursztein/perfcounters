import pytest
import json
from time import sleep
from perfcounters import TimeCounters

def test_prefix():
    cnt_name = "test_a"
    cnts = TimeCounters(prefix='test_')
    cnts.start('a')
    clst = cnts.get_all()
    assert cnt_name in clst
    cnt = cnts.counters['a']
    assert str(cnt) == cnt_name
    assert cnt.__repr__() == cnt_name

def test_e2e():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    cnts.start('b')
    assert len(cnts) == 2

    sleep(D)
    cnts.stop('a')
    assert cnts.get('a') >= D
    sleep(D)
    assert cnts.get('a') < cnts.get('b')
    cnt = cnts.counters['a']
    assert str(cnt) == 'a'
    assert cnt.__repr__() == 'a'

    cnts.stop_all()
    for cnt in cnts.counters.values():
        assert cnt.stop_ts != 0

def test_laps():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    cnts.lap('a')
    sleep(D)
    cnts.lap('a')
    cnts.stop('a')
    assert cnts.get('a') >= D
    assert len(cnts.get_laps('a')) == 3

def test_wrong_stop_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.stop('a')

def test_reset_wrong_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.reset('a')

def test_wrong_lap_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.lap('b')

def test_wrong_get_lap():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.get_laps('b')

def test_wrong_get_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.get('b')


def test_double_start_error():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.start('a')


def test_invalid_format():
    cnts = TimeCounters()
    cnts.start('a')
    with pytest.raises(ValueError):
        cnts.get('a', format='error')


def test_format():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
    assert cnts.get('a', format='m') >= int(D / 60)
    assert cnts.get('a', rounding=0) == 0


def test_json_output():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
    j1 = cnts.to_json(format='ms')
    j2 = cnts.to_json(format='s', rounding=3)
    assert 'a' in j1
    jj = json.loads(j2)
    assert 'a' in jj
    assert jj['a'] < 1

def test_html_output():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
    j1 = cnts.to_html(format='ms')
    assert 'a' in j1
    assert '<table>' in j1



def test_reset():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
    cnts.reset('a')
    assert cnts.get('a') == 0

def test_reset_all():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    cnts.start('b')
    sleep(D)
    assert cnts.get('a', format='ms') >= D * 1000
    cnts.reset_all()
    assert cnts.get('a') == 0
    assert cnts.get('b') == 0


def test_laps_reports():
    D = 0.2
    cnts = TimeCounters()
    cnts.start('a')
    cnts.lap('a')
    sleep(D)
    cnts.lap('a')
    cnts.stop('a')
    assert cnts.get('a') >= D
    assert len(cnts.get_laps('a')) == 3
    cnts.report_laps('a')
    assert  '{' in cnts.laps_to_json('a')


def test_wrong_lap_report_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.lap('a')
        cnts.get_laps('b')

def test_wrong_lap_export_name():
    with pytest.raises(ValueError):
        cnts = TimeCounters()
        cnts.start('a')
        cnts.lap('a')
        cnts.laps_to_json('b')


def test_report():
    cnts = TimeCounters()
    cnts.start('a')
    cnts.start('b')
    assert 'b' in cnts.to_json()
    assert 'b' in cnts.to_html()
    assert 'b' in cnts.to_latex()
    assert 'b' in cnts.to_md()

    cnts.report()


def test_lap_report():
    cnts = TimeCounters()
    cnts.start('a')
    cnts.start('b')
    assert '0' in cnts.laps_to_html('b')
    assert '0' in cnts.laps_to_json('b')
    assert '0' in cnts.laps_to_latex('b')
    assert '0' in cnts.laps_to_md('b')
    cnts.get_laps('b')