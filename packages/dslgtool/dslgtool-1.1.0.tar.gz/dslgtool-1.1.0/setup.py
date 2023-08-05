from setuptools import setup
setup(
    name = 'dslgtool',
    version = '1.1.0',
    packages = ['dslgtool'],
    entry_points = {
        'console_scripts': [
            'dslgtool = dslgtool.__main__:main'
        ]
    })