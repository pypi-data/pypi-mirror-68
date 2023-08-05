from setuptools import find_packages, setup


setup(
    name='aiothrottles',
    version='0.1.1.post1',
    author='Konstantin Togoi',
    author_email='konstantin.togoi@protonmail.com',
    url='https://github.com/KonstantinTogoi/aiothrottles',
    project_urls={'Documentation': 'https://aiothrottles.readthedocs.io'},
    download_url='https://pypi.org/project/aiothrottles/',
    description='Throttles for Python coroutines.',
    long_description=open('README.rst').read(),
    license='BSD',
    packages=find_packages(),
    platforms=['Any'],
    python_requires='>=3.5',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-asyncio'],
    keywords=[
        'asyncio synchronization lock semaphore'
        'throttler throttles throttling rate limiting'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
