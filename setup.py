# setup.py
from setuptools import setup, find_packages

setup(
    name="portmonitor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'PyGObject',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'portmonitor=portmonitor.main:main',
        ],
    },
    data_files=[
        ('share/applications', ['org.mfat.portmonitor.desktop']),
        ('share/metainfo', ['org.mfat.portmonitor.metainfo.xml']),
        ('share/polkit-1/actions', ['org.mfat.portmonitor.policy']),
    ],
    author="mFat",
    author_email="your.email@example.com",
    description="Monitor and manage network ports and their processes",
    license="GPL-3.0",
    keywords="network ports monitor gtk4 libadwaita",
    url="https://github.com/mfat/portsmonitor",
)