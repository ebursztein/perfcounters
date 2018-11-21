# PerfCounters

[![Build Status](https://travis-ci.com/ebursztein/perfcounters.svg?branch=master)](https://travis-ci.com/ebursztein/perfcounters)
[![Coverage Status](https://coveralls.io/repos/github/ebursztein/perfcounters/badge.svg?branch=master)](https://coveralls.io/github/ebursztein/perfcounters?branch=master)
[![license](https://img.shields.io/badge/license-Apache%202-blue.svg?maxAge=2592000)](https://github.com/ebursztein/perfcounters/blob/master/LICENSE)

Easily add performance counters to your python code.

PerfCounter is a thoroughly tested library that make it easy to add multiple counters to any python code to measure intermediate timing and values. Its various reporting mechanisms makes it easy to analyze and report performance measurement regardless of your workflow.

## Installation

The easiest way to install perfcounters is via pip:

```bash
pip install --user -U perfcounters
```

## Type of counter available

Perfcounters natively support two kind of counters: `timing counters` and `value counters`.

### Timing counter usage

Timing counters are used to measure time elapsed in a section of the code. They are started with the `start(...)` method and are stopped with the `stop(...)` method or `stop_all(...)` method.

Here is a simple example:

```python
counters = PerfCounters()  # init counter collection
counters.start('loop')  # start a timing counter

#do something in the code

counters.stop('loop')  # stop counter
counters.report()  # report all counters
```

### Value counter usage

Counters used to track values. They are either directly set to a given value with the `set()` method  or incremented with the `increment()` method. 

Here is a basic example:

```python
counters = PerfCounters()  
counters.set('mycounter', 39)  # set counter value to 39

#do something in the code

counters.increment('mycounter', 3)  # increment counter by 3
counters.get('mycounter') #  get the value of the counter
42
```

## End to end example

Here is an end to end example that demonstrate all the basic feature of the librairy:

```python
from perfcounters import PerfCounters
from random import randint

# init counters
counters = PerfCounters()  

num_iterations = randint(100000, 1000000)

# setting a value counter to a given value
counters.set('num_iterations', num_iterations)

# starting a timing counter
counters.start('loop')

for i in range(1000):
    v = randint(0, 1000000)

    # incrementing a value counter to sum the generated values
    counters.increment('total_value', v)

# stopping a timing counter
counters.stop('loop')

# reporting counters
counters.report()
```

This basic example will produce a result like this:

```bash

-=[Value counters]=-

+----------------+-----------+
| name           |     value |
+================+===========+
| total_value    | 494280557 |
+----------------+-----------+
| num_iterations |    372159 |
+----------------+-----------+

-=[Timing counters]=-

+--------+------------+
| name   |      value |
+========+============+
| loop   | 0.00195169 |
+--------+------------+
```

*Note*: you technically don't need to stop a timing counter before a report. If you don't do it the value reported will be the delta between start time and the time the `report()` function was called. The counter will keep running until it is stopped.

Additional examples are available in the documentation [advanced usage guide](https://github.com/ebursztein/perfcounters/tree/master/docs/advanced_usage.md) and a description of all the available functions are availble in the [API documentation page](https://github.com/ebursztein/perfcounters/tree/master/docs/api.md)

