# PerfCounters

[![Build Status](https://travis-ci.com/ebursztein/perfcounters.svg?branch=master)](https://travis-ci.com/ebursztein/perfcounters)
[![Coverage Status](https://coveralls.io/repos/github/ebursztein/perfcounters/badge.svg?branch=master)](https://coveralls.io/github/ebursztein/perfcounters?branch=master&id=2.0.1)
[![license](https://img.shields.io/badge/license-Apache%202-blue.svg?maxAge=2592000)](https://github.com/ebursztein/perfcounters/blob/master/LICENSE)

Easily add performance counters to your python code.

PerfCounter is a thoroughly tested library that make it easy to add multiple counters to any python code to measure intermediate timing and values. Its various reporting mechanisms makes it easy to analyze and report performance measurement regardless of your workflow.

## Installation

The easiest way to install perfcounters is via pip:

```bash
pip install --user -U perfcounters
```

## Type of counters available

Perfcounters natively support three kind of counters:

- `Timing counters`: used to measure how long a block of code took.
- `Laps counters`: used to measure how each loop iteration take.
- `Value counters`: used to record/track values.

There is currently no way to track value evolution overtime. If it is something
you are interested in, please open an github issue.

## Usage

Here a few example that demonstrate the library basic usage. They are
also available as a [jupyter notebook](https://github.com/ebursztein/perfcounters/blob/master/demo.ipynb).
if you want to follow along. The notebook also contains the advance usage example
so it makes for a convinient reference.

### Timing counter usage

Timing counters are used to measure time elapsed in a section of the code.
They are started with the `start(...)` method and are stopped with
the `stop(...)` method or `stop_all(...)` method.

Here is a short example that uses the timing counters to compare `random()`
versus `randint()` to get a value in  {0, 1}.


```python
counters = PerfCounters()  # init the counter collection.

counters.start('random')  # start a timing counter called random.random.
for x in range(100000):
    int(random.random())
counters.stop('random')  # stop the random.random.

counters.start('randint')  # start a timing counter called random.random.
for x in range(1000000):
    random.randint(0,1)
counters.stop('randint')  # stop the random.random.

counters.report() # report print all counter values in nicely formated tables.
```

This code output a report like this:

```text
-=[Timing counters]=-
+---------+-----------+
| name    |     value |
|---------+-----------|
| randint | 0.982396  |
| random  | 0.0229394 |
+---------+-----------+
```

You can also export the results in various formats including json, text, grepable text and HTML. For example to export in json you can simply use the to_json() function as follow:

```python
counters.to_json()
```

which will return the counters as a json serialized object:

```json
{"Timing counters": [["exponentiation", 0.010947942733764648]]}
```

### Laps counter usage

Timing counters are used to track how long each iteration of a loop is taking. They
work as follow:

```python
counters = PerfCounters()  # declaring our counters

counters.start('random loop') # create counter
for _ in range(3):
    time.sleep(round(random.random(), 2))
    counters.lap('random loop') # record lap time
counters.stop('random loop')

counters.report()  # we don't need to stop the counter. Report do it
```

When outputing/returning laps counters `PerfCounters` do report the value of each lap,
the cumulative time and statistics about the laps:

```text
-=[Timing counters]=-
+-------------+---------+
| name        |   value |
|-------------+---------|
| random loop | 1.57178 |
+-------------+---------+

-=[Laps counters]=-

-= random loop =-
+------------+-------------------+
|   lap time |   cumulative time |
|------------+-------------------|
|   0.760164 |          0.760164 |
|   0.540887 |          1.30105  |
|   0.270732 |          1.57178  |
+------------+-------------------+
+---------+----------+
| stat    |    value |
|---------+----------|
| min     | 0.270732 |
| average | 0.523928 |
| median  | 0.540887 |
| max     | 0.760164 |
| stddev  | 0.200169 |
+---------+----------+
```

*note* you don't need to create a time counter, `Perfcounters` do it for you so
it is easy to track the overall time.

### Value counters usage

Value counters used to track values. They are either directly set to
a given value with the `set()` method  or incremented with the `increment()` method.

Here is a basic example:

```python
counters = PerfCounters()
counters.set('mycounter', 39)  # set counter value to 39
counters.increment('mycounter', 3)  # increment counter by 3
val = counters.get('mycounter') #  get the value of the counter
print('mycounter value:', val)
```

obviously values counters are also report via the `report()` api and exported
along side with the timing counters and laps counters as demonstrated in
the next example.

## Complete example

Here is an end to end example that demonstrate all the basic feature of
`PerfCounters` at once:

```python
from perfcounters import PerfCounters
from random import randint

# init counters
counters = PerfCounters()

num_iterations = randint(5, 10)

# setting a value counter to a given value
counters.set('num_iterations', num_iterations)

# starting a timing counter
counters.start('loop')

for i in range(num_iterations):
    for _ in range(randint(1000, 50000)):
        v = randint(0, 1)

    # incrementing a value counter to sum the generated values
    counters.increment('total_value', v)

    # track lap time
    counters.lap('loop')

# stopping the timing counter
counters.stop('loop')

# reporting all counters
counters.report()
```

This example will produce a result like this:

```text
-=[Value counters]=-
+----------------+---------+
| name           |   value |
|----------------+---------|
| num_iterations |       7 |
| total_value    |       4 |
+----------------+---------+

-=[Timing counters]=-
+--------+----------+
| name   |    value |
|--------+----------|
| loop   | 0.202635 |
+--------+----------+

-=[Laps counters]=-

-= loop =-
+------------+-------------------+
|   lap time |   cumulative time |
|------------+-------------------|
| 0.0358815  |         0.0358815 |
| 0.00401258 |         0.0398941 |
| 0.0359035  |         0.0757976 |
| 0.0398953  |         0.115693  |
| 0.038939   |         0.154632  |
| 0.0100079  |         0.16464   |
| 0.0379953  |         0.202635  |
+------------+-------------------+
+---------+------------+
| stat    |      value |
|---------+------------|
| min     | 0.00401258 |
| average | 0.0289479  |
| median  | 0.0359035  |
| max     | 0.0398953  |
| stddev  | 0.014033   |
+---------+------------+
```

*Note*: you technically don't need to stop a timing counter before a report. If you don't do it the value reported will be the delta between start time and the time the `report()` function was called. The counter will keep running until it is stopped.

## Advanced usages

- Additional examples are available in the documentation [advanced usage guide](https://github.com/ebursztein/perfcounters/tree/master/docs/advanced_usage.md).
- A description of all the available functions are availble in the [API documentation page](https://github.com/ebursztein/perfcounters/tree/master/docs/api.md)