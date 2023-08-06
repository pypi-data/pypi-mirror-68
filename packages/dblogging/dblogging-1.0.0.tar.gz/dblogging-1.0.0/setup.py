__version__ = "1.0.0"

from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='dblogging',
        packages=find_packages(where='.', exclude=['testing']),
        package_dir={
            'dblogging': 'dblogging'
        },
        include_package_data=True,
        description='Persist logs With SQLite. Easy to query logs.',
        version=__version__,
        author='Tyler Spens',
        author_email='mrtspens@gmail.com',
        keywords=['logging', 'persistent', 'database', 'db'],
        install_requires=[
            'jsonpickle',
            'Pygments',
            'htmlmin'
        ],
        url='https://gitlab.com/tspens/thelogger',
        download_url='https://gitlab.com/tspens/thelogger/-/archive/v1.0/thelogger-v1.0.tar.gz',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.8',
        ]
    )
