from setuptools import setup, find_packages

setup(
    name='HealthUpdates',
    version='0.1.1',
    license='Creative Commons Attribuion-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    entry_points={'console_scripts': [
        'hupdater=healthupdates.updates:main'
    ]
    },
)
