from setuptools import setup

setup(
    name='cloud_linux',
    version='0.0.1',
    install_requires=[
        'canvasapi',
        'pyyaml',
        'importlib-metadata; python_version == "3.10"',
    ],
    packages=['cloud_linux'],
)
