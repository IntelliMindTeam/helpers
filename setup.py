import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="common_utils_rajan shah",
    version="0.0.1",
    author="Rajan Shah",
    author_email="rajan@intellimind.io",
	license="MIT",
    description="general-utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IntelliMindTeam/common-utils.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
	install_requires=[
        'argparse',
        'arctic',
        'boto3',
        'bs4',
        'csv',
        'datetime',
        'dateutil'
        'hashlib'
        'holidays'
        'hmac'
        'influxdb'
        'json',
        'logging',
        'lxml'
        'mock'
        'nltk'
        'pandas'
        'pymysql',
        'redis'
        'rethinkdb',
        'requests'
        'urllib2'
        'socket'
        'string'
        'sklearn',
        
        ],
    dependency_links=[
        # link of pip installation from github without git+
        ],

)

