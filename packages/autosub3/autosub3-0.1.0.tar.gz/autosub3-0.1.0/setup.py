#!/usr/bin/env python


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = (
    'This project upgrades original autosub and adds support for windows.'
    'Autosub is a utility for automatic speech recognition and subtitle generation. '
    'It takes a video or an audio file as input, performs voice activity detection '
    'to find speech regions, makes parallel requests to Google Web Speech API to '
    'generate transcriptions for those regions, (optionally) translates them to a '
    'different language, and finally saves the resulting subtitles to disk. '
    'It supports a variety of input and output languages (to see which, run the '
    'utility with --list-src-languages and --list-dst-languages as arguments '
    'respectively) and can currently produce subtitles in either the SRT format or '
    'simple JSON.'
)

setup(
    name='autosub3',
    version='0.1.0',
    description='Auto-generates subtitles for any video or audio file',
    long_description=long_description,
    author='jiaox99',
    author_email='jiaox99@163.com',
    url='https://github.com/jiaox99/autosub',
    packages=['autosub'],
    entry_points={
        'console_scripts': [
            'autosub = autosub:main',
        ],
    },
    install_requires=[
        'google-api-python-client>=1.4.2',
        'requests>=2.3.0',
        'pysrt>=1.0.1',
        'progressbar2>=3.34.3',
        'six>=1.11.0',
    ],
    license=open("LICENSE").read()
)
