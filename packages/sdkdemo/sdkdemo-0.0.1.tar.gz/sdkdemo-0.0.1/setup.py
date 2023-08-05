# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
from setuptools import setup
kwargs = {}

version = "0.0.1"

setup(name="sdkdemo",
      version=version,
      packages=["sdkdemo"],
      package_data={'': ['*.*']},
      author="comger@gmail.com",
      author_email="comger@gmail.com",
      url="http://github.com/comger/kpages",
      license="http://www.apache.org/licenses/LICENSE-2.0",
      description="Demo SDK for gitlab ci auto pub",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      **kwargs)
