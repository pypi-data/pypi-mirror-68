#!/usr/bin/env python3

from setuptools import setup, find_packages

import vertool


# Get long description about this python project.
with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='vertool',
    version=vertool.__version__,
    python_requires='>=3.4',
    url='https://bitbucket.org/celadonteam/vertool',
    author='Celadon Developers',
    author_email='opensource@celadon.ae',
    description='The project versioning controller',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    scripts=['vertool/__main__.py'],
    entry_points={
        'console_scripts': [
            'vertool=vertool.__main__:main',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development',
    ],
)
