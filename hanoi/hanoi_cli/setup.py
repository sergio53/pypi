import setuptools as st

st.setup(
    name='hanoi_cli',
    version='1.0.0',
    py_modules=['hanoi_cli'],
    entry_points={
       'console_scripts':
           'hanoi_cli=hanoi_cli:main',
    },
)
