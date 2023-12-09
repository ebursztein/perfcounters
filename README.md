# PerfCounters

[![Coverage Status](https://coveralls.io/repos/github/ebursztein/perfcounters/badge.svg?branch=master)](https://coveralls.io/github/ebursztein/perfcounters?branch=master&id=2.0.1)
[![license](https://img.shields.io/badge/license-Apache%202-blue.svg?maxAge=2592000)](https://github.com/ebursztein/perfcounters/blob/master/LICENSE)

Easily add performance counters to your python code.

PerfCounter is a thoroughly tested library that make it easy to add counters to
any python code to measure intermediate timings and values.
Its various reporting mechanisms (pretty print, json, html, latex, markdown... )
makes it easy to analyze and report performance measurement regardless of
your workflow.

Perfcounters natively support two kind of counters:

- `TimeCounters()` that are used to track timings.
- `ValueCounters()` thatr used if you want to track values.

For each counter you can track intermediate values using the `lap()` API
if needed.

## Basic usage
Here is a short example that demonstrate how to track time. Tracking values
looks very similarly.

```python
import random
from perfcounters import TimeCounters

cnts = TimeCounters()  # init the counter collection.

cnts.start('random')  # start a timing counter called random.
for x in range(100000):
    int(random.random())
cnts.stop('random')  # stop the random counter

cnts.start('randint')  # start a timing counter called randint.
for x in range(1000000):
    random.randint(0, 1)
cnts.stop('randint')  # stop the randint counter.

cnts.report(rounding=5) # report print all counter values in a nicely formated table.
```

For more advanced usage take look at
the [demo jupyter notebook](https://github.com/ebursztein/perfcounters/blob/master/demo.ipynb).

## Installation

The easiest way to install perfcounters is via pip:

```bash
pip install --user -U perfcounters
```
