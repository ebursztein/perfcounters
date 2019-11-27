"display functions"
from __future__ import absolute_import
import json

from .report import gen_report, process_counters
from .report import TIME_COUNTERS, VALUE_COUNTERS, LAPS_COUNTERS


def to_json(counters, laps):
    """Export counters result as json

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.

    Returns:
        str: JSON representation
    """
    pcounters = process_counters(counters, laps, 'value', True)
    return json.dumps(pcounters)


def report(counters, laps, sort_by='value', reverse=True):
    """Print counters in stdout as nicely formated tables.

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True.
    """
    print(to_text(counters, laps, sort_by, reverse))


def to_text(counters, laps, sort_by='value', reverse=True):
    """Return counters asnicely formated text
    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True.
    """
    return gen_report(counters, laps, sort_by, reverse, 'text')


def to_html(counters, laps, sort_by='value', reverse=True):
    """Return counters in HTML format.

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True.
    """
    return gen_report(counters, laps, sort_by, reverse, 'html')


def to_grepable_text(counters, laps, sort_by, reverse):
    """Return counters in a grepable format

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True
    """
    report = ''

    pcounters = process_counters(counters, laps, sort_by, reverse)
    for ctype in [VALUE_COUNTERS, TIME_COUNTERS]:
        if ctype in pcounters:
            for cnt in pcounters[ctype]:
                report += "[PerfCounters]%s:%s:%s\n" % (ctype, cnt[0], cnt[1])

    if LAPS_COUNTERS in pcounters:
        for data in pcounters[LAPS_COUNTERS]:
            report += "[Perfcounter]%s:%s:laps:%s\n" % (LAPS_COUNTERS,
                                                        data['name'],
                                                        data['laps'])

            stats = ["%s=%s" % (k, v) for k, v in data['stats'].items()]
            stats = ','.join(stats)
            report += "[Perfcounter]%s:%s:stats:%s\n" % (LAPS_COUNTERS,
                                                         data['name'],
                                                         stats)

    return report
