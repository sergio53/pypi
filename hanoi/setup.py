import setuptools

setuptools.setup(
    name='hanoi',
    version='1.0.0',
    packages=['hanoi'],
    entry_points={
       'console_scripts':
           'hanoi=hanoi:main',
    },
)