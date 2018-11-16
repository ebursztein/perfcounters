from setuptools import setup
from setuptools import find_packages

long_description = '''
PerfCounter allows to add easily add and report multiple performance counters
to any python code to measure intermediate performance and values.
'''

setup(name='PerfCounters',
      version='1.0.0',
      description='Easily add performance counters to your code',
      long_description=long_description,
      author='Elie Bursztein',
      author_email='code@elie.net',
      url='https://github.com/ebursztein/PerfCounters',
      license='Apache 2',
      install_requires=['tabulate'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Debuggers',
          'Topic :: Software Development :: Testing'
      ],
      packages=find_packages())