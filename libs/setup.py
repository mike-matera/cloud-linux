from setuptools import setup

setup(
    name='cloud_linux',
    version='0.0.2',
    install_requires=[
        'canvasapi',
        'pynacl',
        'pyyaml',
        'psutil',
        'importlib-metadata; python_version == "3.10"',
    ],
    packages=['cloud_linux', 'cloud_linux.labs'],
)
