# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='weixin',
    version='0.1.0',

    description='A weixin api project',
    long_description=long_description,

    url='https://github.com/ujsxn/weixin',

    author='Nan Xiang',
    author_email='514580344@qq.com',

    license='GPLv3',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='weixin wechat api',

    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['requests', 'redis'],

)