from setuptools import setup

setup(
    name='cloud_linux',
    version='0.1.6',
    install_requires=[
        'canvasapi',
        'pynacl',
        'pyyaml',
        'psutil',
        'importlib-metadata; python_version == "3.10"',
    ],
    packages=['cloud_linux', 'cloud_linux.labs'],
    entry_points={
        'console_scripts': [
            'secrets = cloud_linux.secrets:main',
        ]
    },
)
