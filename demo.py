from perfcounters import PerfCounters
from random import randint

print("=== Basic usage ===\n")

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

print("\n=== Sorting ===\n")
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

print("=== Reporting ===\n")
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


print("\n=== Counters merging ===\n")

counters = PerfCounters()
counters.set('test', 42)

# set counter prefix via constructor to avoid name collision
other_counters = PerfCounters('others')
other_counters.set('test', 42)

#merging
counters.merge(other_counters)
counters.report()