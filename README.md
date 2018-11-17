# PerfCounters

Easily add performance counters to your python code.

PerfCounter make it easy to add multiple performance counters to any python code to measure 
intermediate performance and values.

## Basic example

```python
from perfcounters import PerfCounters
from random import randint

counters = PerfCounters() # init counters
counters.start('loop') # start a timing counter
for i in range(1000):
    v = randint(0, 1000000)
    counters.increment('total_value', v) # use a value counter to sum generated value
counters.stop('loop') # stop timing counter
counters.report() # report counter
```

This basic example should produce a result like this:

```bash
-=[Timing counters]=-

+--------+-------------+
| name   |       value |
+========+=============+
| loop   | 0.000996351 |
+--------+-------------+

-=[Value counters]=-

+-------------+-----------+
| name        |     value |
+=============+===========+
| total_value | 477520648 |
+-------------+-----------+
```