from setuptools import setup

setup(
    name='cman',
    version='0.1.0',
    description='Container manager',
    url='https://github.com/MatthewScholefield/cman',
    maintainer='Matthew D. Scholefield',
    maintainer_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cman',
    py_modules=['cman'],
    install_requires=[
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'cman=cman:main'
        ],
    }
)
