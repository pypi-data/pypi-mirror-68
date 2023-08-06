#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()
    example_start = readme.find('PyFreya Example')  # remove example part from README
    readme = readme[:example_start]

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# Load requirements.txt file and read it.
try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        raise ImportError('Could not import pip methods for including requirements.txt')

requirements = parse_requirements('requirements.txt', session=PipSession())

requires = []

for item in requirements:
    # if item.req:
    requires.append(str(item.req))


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Morten Andreasen",
    author_email='yggdrasil.the.binder@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Cohort Analysis Tool",
    install_requires=requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyfreya',
    name='pyfreya',
    packages=find_packages(include=['pyfreya', 'pyfreya.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/Yggdrasil27/pyfreya',
    version='0.3.0',
    zip_safe=False,
    PROJECT_URLS={
        "Bug Tracker": "https://gitlab.com/Yggdrasil27/pyfreya/-/issues",
        "Documentation": "https://pyfreya.readthedocs.io/en/latest/",
    },
)
