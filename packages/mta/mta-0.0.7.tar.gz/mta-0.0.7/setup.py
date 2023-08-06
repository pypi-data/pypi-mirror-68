from setuptools import setup
import os

setup(name='mta',
      version='0.0.7',
      description='Multi-Touch Attribution',
      classifiers=[
      	'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3.6'
      ],
      url='https://github.com/eeghor/mta',
      author='Igor Korostil',
      author_email='eeghor@gmail.com',
      license='MIT',
      packages=['mta'],
      python_requires='>=3.6',
      package_data={'mta': ['data/*.csv.gz']},
      keywords='attribution marketing')