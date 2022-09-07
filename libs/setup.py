from setuptools import setup

setup(
    name='cloud_linux',
    version='0.0.1',
    install_requires=[
        'canvasapi',
        'nacl',
        'pyyaml',
        'psutil',
        'importlib-metadata; python_version == "3.10"',
    ],
    packages=['cloud_linux', 'cloud_linux.labs'],
)
