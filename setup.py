from setuptools import setup
from setuptools import find_packages

long_description = open("README.md").read()
version = '1.0.5'
setup(name='perfcounters',
      version=version,
      description='Easily add performance counters to your code',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Elie Bursztein',
      author_email='code@elie.net',
      url='https://github.com/ebursztein/perfcounters',
      license='Apache 2',
      install_requires=[
          'tabulate',
          'numpy'],
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
