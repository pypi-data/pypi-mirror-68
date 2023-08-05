import pathlib
import setuptools


VERSION = '1.0.0b0'
ROOT = pathlib.Path('.')


with open(ROOT / 'README.md') as f:
    long_description = f.read()


metadata = dict(
    name='pipedrivepy',
    packages=['pipedrive'],
    version=VERSION,
    description='Pipedrive API Generic Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Pipedrive, python, API',
    author='Vitalii Maslov',
    author_email='hello@bindlock.me',
    url='https://github.com/bindlock/pipedrivepy',
    download_url='https://github.com/bindlock/pipedrivepy/tarball/master',
    license='MIT',
    extras_require={'sync': ['requests'], 'async': ['aiohttp']},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)


setuptools.setup(**metadata)
