from setuptools import setup, find_packages
import os
import subprocess

version_file = 'src/masonite/interfaces/version.txt'

if not os.path.exists(version_file):
    with open(version_file, 'w') as file:
        file.write(os.getenv('CIRCLE_TAG', '0.0.1-dev').replace('v', ''))

with open(version_file) as file:
    version = file.read()

setup(
    name="masonite-interfaces",
    packages=[
        'masonite.interfaces',
    ],
    package_dir={'': 'src'},
    version=version,
    install_requires=[],
    description="Interface Package",
    author="Joseph Mancuso",
    author_email='joe@masoniteproject.com',
    url='https://github.com/MasoniteFramework/masonite',
    keywords=['masonite', 'python web framework', 'python3'],
    license='MIT',
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ]
)
