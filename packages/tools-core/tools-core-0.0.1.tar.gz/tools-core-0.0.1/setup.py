import os
from setuptools import setup

requirements = [
    "pymongo>=3.7",
    "python-decouple>=3.1",
    "redis",
    "pycrypto==2.6.1",
    "pymysql",
    "elasticsearch-dsl==6.3.1",
    "pika==0.12",
    "shortuuid",
    "requests",
    "threadpool>=1.3.2",
    "python-dateutil>=2.7",
    "sqlalchemy>=1.2",
    "aliyun-python-sdk-core-v3"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tools-core',
    version='0.0.1',
    packages=[
            "tools_core",
    ],
    license='BSD License',  # example license
    description='tools core',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='',
    author='lijun35',
    author_email='m18252063675@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)