from setuptools import setup
from setuptools import find_packages

long_description = '''
PerfCounter is a thoroughly tested library that make it easy to add multiple
counters to any python code to measure intermediate timing and values.

Its various reporting mechanisms makes it easy to analyze and
report performance measurement regardless of your workflow.
'''

setup(name='perfcounters',
      version='1.0.0',
      description='Easily add performance counters to your code',
      long_description=long_description,
      author='Elie Bursztein',
      author_email='code@elie.net',
      url='https://github.com/ebursztein/perfcounters',
      license='Apache 2',
      install_requires=['tabulate'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Debuggers',
          'Topic :: Software Development :: Testing'
      ],
      packages=find_packages())
