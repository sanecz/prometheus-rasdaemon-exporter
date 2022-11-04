from setuptools import find_packages, setup

from os import path

top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='prometheus-rasdaemon-exporter',
    version='1.0.0',
    description='Prometheus exporter for rasdaemon',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'prometheus-client>=0.15.0'
    ],
    entry_points={
        'console_scripts': [
            'prometheus-rasdaemon-exporter = prometheus_rasdaemon_exporter.rasdaemon_exporter:main',
        ],
    },
    packages=["prometheus_rasdaemon_exporter"],
    include_package_data=True,
    keywords=['prometheus', 'rasdaemon', 'monitoring'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Monitoring',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
