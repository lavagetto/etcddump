from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.0.1'

install_requires = [
    'python-etcd>=0.3.0',
]


setup(name='etcddump',
    version=version,
    description="A dump tool for etcd",
    classifiers=[
        "Topic :: System :: Distributed Computing",
        "Topic :: Database :: Front-Ends",
        "Topic :: System :: Recovery Tools",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ],
    long_description=README,
    keywords='etcd datastore dumper program',
    author='Giuseppe Lavagetto',
    author_email='lavagetto@gmail.com',
    url='http://github.com/lavagetto/etcddump',
    license='GPL3',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'etcdumper = etcddump.cli:main',
    ],
  },

)
