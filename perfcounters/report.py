# display utility functions
import time
from collections import defaultdict
from operator import itemgetter
import numpy as np
from tabulate import tabulate
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

VALUE = 1
TIME = 2
LAP = 3

VALUE_COUNTERS = 'Value counters'
TIME_COUNTERS = 'Timing counters'
LAPS_COUNTERS = 'Laps counters'


def gen_report(counters, laps, sort_by, reverse, report_format):
    """Convert counter data in tables that can be easily displayed

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True.
        report_format (str): Report format type. html, text, markdown, latex

    Returns:
        str: Report formated in the requested format
    """

    # processing counters
    pcounters = process_counters(counters, laps, sort_by, reverse)

    # selecting table format
    if report_format == 'text':
        table_format = 'psql'
    elif report_format == 'html':
        table_format = 'html'
    elif report_format == 'markdown':
        table_format = 'github'
    elif report_format == 'latex':
        table_format = 'latex'

    report = ""
    # time and value counters
    for cnt_type in [VALUE_COUNTERS, TIME_COUNTERS]:
        if cnt_type in pcounters:
            report += _gen_header(cnt_type, 1, report_format)
            headers = ["name", "value"]
            report += tabulate(pcounters[cnt_type], headers=headers,
                               tablefmt=table_format)
            if report_format == 'text':
                report += '\n\n'

    # laps
    if LAPS_COUNTERS in pcounters:
        report += _gen_header(LAPS_COUNTERS, 1, report_format)
        for laps_counter in pcounters[LAPS_COUNTERS]:

            # laps
            if report_format == 'text':
                report += '\n'
            report += _gen_header(laps_counter['name'], 2, report_format)
            headers = ['lap time', 'cumulative time']
            report += tabulate(laps_counter['laps'], headers=headers,
                               tablefmt=table_format)

            # stats
            if report_format == 'text':
                report += '\n'
            headers = ['stat', 'value']
            stats = [[k, v] for k, v in laps_counter['stats'].items()]
            report += tabulate(stats, headers=headers, tablefmt=table_format)

        if report_format == 'text':
            report += '\n'

    return report


def _gen_header(value, level, report_format):
    """Generate header in the requested format

    Args:
        value (str): Header value.
        level (int): Indent level 1,2,3 -> h1, h2, h3 / #, ##, ### ...
        report_format (str): Format type: text, html, markdown, latex ...
    Returns:
        str: formated header as string
    """
    if report_format == 'text':
        if level == 1:
            stub_in = '-=['
            stub_out = ']=-'
        else:
            stub_in = '-= '
            stub_out = ' =-'
        return "%s%s%s\n" % (stub_in, value, stub_out)
    elif report_format == 'html':
        return "<h%s>%s</h%s>\n" % (level, value, level)
    elif report_format == 'markdown':
        stub = '#' * level
        return "%s%s\n" % (stub, value)
    else:
        raise Exception('Unknown report format: ', report_format)


def process_counters(counters, laps, sort_by='value', reverse=True):
    """ Compute the internal representation of the counters used by all output

    Args:
        counters (dict): Collection of counters to process.
        laps (dict): Collection of laps to process.
        sort_by (str, optional): How to sort the counters. Defaults to 'value'.
        reverse (bool, optional): Reverse the sorting. Defaults to True.
    """

    processed_counters = defaultdict(list)
    laps_counters = []  # merge at the end to make the code simpler

    # process counters
    for name, data in counters.items():

        if data['type'] == VALUE:
            processed_counters[VALUE_COUNTERS].append([name, data['value']])

        elif data['type'] == TIME or data['type'] == LAP:

            # needed to allow to display counters as they progress
            if 'stop' not in data:
                stop = time.time()
            else:
                stop = data['stop']
            delta = stop - data['start']
            processed_counters[TIME_COUNTERS].append([name, delta])

        # additional computation
        if data['type'] == LAP:
            progression, stats = _compute_lap_stats(laps[name], data['start'])
            laps_counters.append(
                {
                    'name': name,
                    'stats': stats,
                    'laps': progression
                }
            )

    # sorting
    if sort_by == 'value':
        SORT_IDX = 1
    else:
        SORT_IDX = 0

    for k, v in processed_counters.items():
        processed_counters[k] = sorted(v, key=itemgetter(SORT_IDX),
                                       reverse=reverse)

    # adding laps if needed
    if len(laps_counters):
        processed_counters[LAPS_COUNTERS] = laps_counters

    return processed_counters


def _compute_lap_stats(laps, start_time):
    """compute laps value and statistics

    Args:
        laps (list): list of recorded time
        start_time (float): time of the initial recording

    Returns:
        list: report, stats
    """

    # getting initial time
    previous_time = start_time

    # computing deltas
    deltas = []
    report = []  # report delta and cumulative time
    cumulative_time = 0
    for timing in laps:
        delta = timing - previous_time
        cumulative_time += delta
        deltas.append(delta)
        report.append([delta, cumulative_time])
        previous_time = timing

    # compute stats
    stats = {
        "min": np.min(deltas),
        "average": np.average(deltas),
        "median": np.median(deltas),
        "max": np.max(deltas),
        "stddev": np.std(deltas)
    }

    return report, stats
