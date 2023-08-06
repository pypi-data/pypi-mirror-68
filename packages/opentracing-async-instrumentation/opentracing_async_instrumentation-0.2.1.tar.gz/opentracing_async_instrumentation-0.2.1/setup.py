from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='opentracing_async_instrumentation',
    version='0.2.1',
    author='Jessie Morris',
    author_email='jessie.m@midigator.com',
    description='Async Tracing Instrumentation using OpenTracing API '
                '(http://opentracing.io)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitlab.com/midigator/python_opentracing_async_instrumentation/',
    keywords=['opentracing', 'async', 'asyncio'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    install_requires=[
        'future',
        'wrapt',
        'contextlib2',
        'opentracing>=2,<3',
        'six',
    ],
    extras_require={
        'tests': [
            'aiohttp',
            'aiobotocore',
            'aioboto3',
            'aiomysql',
            'basictracer>=3,<4',
            'flake8',
            'mock',
            'moto[server]',
            'pytest',
            'pytest-cov',
            'pytest-localserver',
            'pytest-mock',
            'pytest-asyncio',
            'pytest-aiohttp',
            'testfixtures',
            'tox',
        ]
    },
)
