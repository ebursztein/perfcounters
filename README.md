[![Build Status](https://travis-ci.com/ebursztein/perfcounters.svg?branch=master)](https://travis-ci.com/ebursztein/perfcounters)
[![Coverage Status](https://coveralls.io/repos/github/ebursztein/perfcounters/badge.svg?branch=master)](https://coveralls.io/github/ebursztein/perfcounters?branch=master)
[![license](https://img.shields.io/badge/license-Apache%202-blue.svg?maxAge=2592000)](https://github.com/ebursztein/perfcounters/blob/master/LICENSE)

# PerfCounters

Easily add performance counters to your python code.

PerfCounter is a thoroughly tested library that make it easy to add multiple counters to any python code to measure intermediate timing and values. Its various reporting mechanisms makes it easy to analyze and report performance measurement regardless of your workflow.

## Installation

The easiest way to install perfcounters is via pip:

```bash
pip install --user -U perfcounters
```

## Basic usage

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

*Note*: you technically don't need to stop a counter before a report. If you don't do it the value reported will be the delta between start time and the
time the `report()` function as called. The counter will keep running until it is stopped.

## Advanced usage examples

Here are a few examples that demonstrate the advanced options the library. All the examples showcased in this section are available in the [demo script](https://github.com/ebursztein/perfcounters/blob/master/demo.py)

### Sorting counters

By default counters are sorted by "value desc". You can change this behavior with the optional arguments available in all reporting functions (report(), to_html(), log()..). here is a short example:

```python
counters = PerfCounters()
counters.set('a', 42)
counters.set('b', 40)
counters.set('c', 41)

print("sort by value desc (default)")
counters.report()

print("sort by value asc")
counters.report(reverse=False)

print("sort by name desc")
counters.report(sort_by=PerfCounters.SORT_BY_NAME)

print("sort by name asc")
counters.report(sort_by=PerfCounters.SORT_BY_NAME, reverse=False)
```

This produce the following expected results:


#### sort by value desc (default)

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| a      |      42 |
+--------+---------+
| c      |      41 |
+--------+---------+
| b      |      40 |
+--------+---------+
```

#### sort by value asc

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| b      |      40 |
+--------+---------+
| c      |      41 |
+--------+---------+
| a      |      42 |
+--------+---------+
```

#### sort by name desc

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| c      |      41 |
+--------+---------+
| b      |      40 |
+--------+---------+
| a      |      42 |
+--------+---------+
```

#### sort by name asc

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| a      |      42 |
+--------+---------+
| b      |      40 |
+--------+---------+
| c      |      41 |
+--------+---------+
```

### Reporting options

Beside printing in terminal `perfcounters` offers multiple reporting options. Here are the main ones:

```python
counters = PerfCounters()
counters.start('loop')
for i in range(1000):
    v = randint(0, 1000000)
    counters.increment('total_value', v)
counters.stop('loop')

print("Terminal output")
counters.report()

print("HTML output")
print(counters.to_html())

print("JSON output")
print(counters.to_json())

print("Log output")
counters.log()
```

#### HTML output

```html
Timing counters</br><table>
<thead>
<tr><th>name  </th><th style="text-align: right;">     value</th></tr>
</thead>
<tbody>
<tr><td>loop  </td><td style="text-align: right;">0.00195193</td></tr>
</tbody>
</table></br>Value counters</br><table>
<thead>
<tr><th>name       </th><th style="text-align: right;">    value</th></tr>
</thead>
<tbody>
<tr><td>total_value</td><td style="text-align: right;">493950295</td></tr>
</tbody>
</table></br>
```

#### JSON output

```json
{
  "Timing counters": [
    [
      "loop",
      0.0019519329071044922
    ]
  ],
  "Value counters": [
    [
      "total_value",
      493950295
    ]
  ]
}
```

### Restarting a timer



### Merging counters

```python
counters = PerfCounters()
counters.set('test', 42)

# set counter prefix via constructor to avoid name collision
other_counters = PerfCounters('others')
other_counters.set('test', 42)
counters.report()
```

output:

```bash
-=[Value counters]=-

+-------------+---------+
| name        |   value |
+=============+=========+
| test        |      42 |
+-------------+---------+
| others_test |      42 |
+-------------+---------+
```

*note*: if two counters have the same name `PerfCounters` will raise a `ValueError`. To avoid name collision you can set a counter prefix in the constructor like so: `PerfCounters("prefix")`.

### Getting the numbers of counters

```python
counters = PerfCounters()
counters.set('test', 42)
print(len(counters))
```